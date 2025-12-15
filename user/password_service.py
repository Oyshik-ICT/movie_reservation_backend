import hashlib
import secrets
import time
from datetime import datetime

from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from .models import CustomUser
from .serializers import CustomUserSerializer


class PasswordResetThrottle(AnonRateThrottle):
    rate = "3/min"


class PasswordResetService:
    @staticmethod
    def generate_secure_token():
        return secrets.token_urlsafe(32)

    @staticmethod
    def check_rate_limit_per_email(email):
        attempts = cache.get(email, 0)
        if attempts > 3:
            return False
        cache.set(email, attempts + 1, timeout=3600)

        return True

    @staticmethod
    def generate_secure_pin():
        """Generate cryptographically secure 6-digit PIN"""
        return "".join([str(secrets.randbelow(10)) for _ in range(6)])

    @staticmethod
    def hash_token(token):
        """Hash tokens before storing (OWASP security practice)"""
        return hashlib.sha256(token.encode()).hexdigest()

    @staticmethod
    def send_reset_pin_email(email, secure_pin):
        send_mail(
            subject="Password Reset Verification Code",
            message=f"""Your password reset verification code is: {secure_pin}

    This code will expire in 15 minutes.
    If you did not request this reset, please ignore this email.

    For security, this code can only be used once.""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

    @staticmethod
    def _ensure_consistent_timing(start_time):
        elapsed = time.time() - start_time
        if elapsed < 0.5:  # Minimum 500ms response time
            time.sleep(0.5 - elapsed)

    @classmethod
    def initiate_password_reset(cls, email):
        start_time = time.time()
        # Standard response message (no user enumeration)
        STANDARD_MESSAGE = "If an account with this email exists, you will receive a password reset code shortly."
        ERROR_MESSAGE = (
            "We're experiencing technical difficulties. Please try again later."
        )
        RATE_LIMIT_MESSAGE = "Too many reset requests. Please try again later."

        try:
            # Always perform the same operations regardless of user existence
            # This prevents timing attacks and user enumeration

            # Check rate limiting per email
            if not PasswordResetService.check_rate_limit_per_email(email):
                cls._ensure_consistent_timing(start_time)
                return False, RATE_LIMIT_MESSAGE, "rate_limit"

            # Always generate token and perform database lookup (prevent timing attacks)
            secure_token = PasswordResetService.generate_secure_token()
            secure_pin = PasswordResetService.generate_secure_pin()

            try:
                user = CustomUser.objects.get(email=email)
                user_exists = True
            except CustomUser.DoesNotExist:
                user_exists = False
                # Create dummy user object to maintain consistent timing
                user = type("DummyUser", (), {"pk": 0, "email": email})

            if user_exists:
                # Clear any existing reset tokens for this user
                cache.delete(f"pwd_reset_user:{user.pk}")

                # Store hashed token with user data
                token_data = {
                    "user_id": user.pk,
                    "email": email,
                    "pin": secure_pin,
                    "created_at": datetime.now().isoformat(),
                    "attempts": 0,
                    "used": False,
                }

                # Store with hashed token as key (OWASP recommended)
                hashed_token = PasswordResetService.hash_token(secure_token)
                cache.set(
                    f"pwd_reset_token:{hashed_token}", token_data, timeout=900
                )  # 15 minutes

                # Also store user-to-token mapping for cleanup
                cache.set(f"pwd_reset_user:{user.pk}", hashed_token, timeout=900)

                # Send PIN via email (OWASP: side-channel communication)
                cls.send_reset_pin_email(email, secure_pin)

            # Ensure consistent response time (prevent timing attacks)
            cls._ensure_consistent_timing(start_time)

            return True, STANDARD_MESSAGE, None

        except Exception as e:
            # Log error but don't expose it (security)
            # logger.error(f"Password reset error: {e}")

            # Ensure consistent response time even on errors
            cls._ensure_consistent_timing(start_time)
            return False, ERROR_MESSAGE, str(e)

    @classmethod
    def verify_reset_pin(cls, email, pin):
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return False, "Invalid credentials", None

        user_token_hash = cache.get(f"pwd_reset_user:{user.pk}")
        if not user_token_hash:
            return False, "No active reset request found", None

        token_data = cache.get(f"pwd_reset_token:{user_token_hash}")
        if not token_data:
            return False, "Reset request expired", None

        if token_data["pin"] != pin:
            token_data["attempts"] += 1

            # Lock after 3 failed attempts (OWASP: brute force protection)
            if token_data["attempts"] > 3:
                cache.delete(f"pwd_reset_token:{user_token_hash}")
                cache.delete(f"pwd_reset_user:{user.pk}")
                return (
                    False,
                    "Too many failed attempts. Please request a new reset code.",
                    None,
                )

            cache.set(f"pwd_reset_token:{user_token_hash}", token_data, timeout=900)
            return Response(
                {
                    "error": f"Invalid PIN. {3 - token_data['attempts']} attempts remaining."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if already used
        if token_data["used"]:
            return False, "Reset code already used", None

        # PIN verified - generate reset session token
        reset_token = cls.generate_secure_token()
        reset_data = {
            "user_id": user.pk,
            "email": email,
            "verified": True,
            "created_at": datetime.now().isoformat(),
        }

        # Store reset session (10 minutes)
        hashed_reset_token = cls.hash_token(reset_token)
        cache.set(f"pwd_reset_session:{hashed_reset_token}", reset_data, timeout=600)

        # Mark PIN as used and clean up
        token_data["used"] = True
        cache.set(f"pwd_reset_token:{user_token_hash}", token_data, timeout=900)

        return True, "PIN verified successfully", reset_token

    @classmethod
    def reset_password(cls, reset_token, new_password):
        # Get reset session
        hashed_token = cls.hash_token(
            reset_token,
        )
        reset_data = cache.get(f"pwd_reset_session:{hashed_token}")

        if not reset_data or not reset_data.get("verified"):
            return False, "Invalid or expired reset session"

        try:
            user = CustomUser.objects.get(pk=reset_data["user_id"])
            serializer = CustomUserSerializer(
                user, data={"password": new_password}, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            cache.delete(f"pwd_reset_session:{hashed_token}")
            cache.delete(f"pwd_reset_user:{user.pk}")

            # Send notification email (OWASP: notify user of password change)
            send_mail(
                subject="Password Successfully Reset",
                message=f"""Your password has been successfully reset.

    If you did not perform this action, please contact support immediately.

    Reset performed on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,  # Don't fail if email fails
            )

            return (
                True,
                "Password reset successfully. Please log in with your new password.",
            )

        except CustomUser.DoesNotExist:
            return False, "User not found"
        except serializers.ValidationError as e:
            return False, e.detail
