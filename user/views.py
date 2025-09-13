from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from .models import CustomUser
from .serializers import CustomUserSerializer, CustomAdminUserSerializer, ForgetPasswordSerializer, ResetPasswordSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsAdmin
from rest_framework.decorators import api_view
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
import secrets
from django.core.cache import cache
from rest_framework.decorators import api_view, throttle_classes
from .password_service import PasswordResetThrottle, PasswordResetService
from datetime import datetime, timedelta
import hashlib
import time


class UserViewset(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()
    
    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        qs = qs.filter(email=user.email)

        return qs
    
class AdminUserViewset(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomAdminUserSerializer
    permission_classes = [IsAdmin]
    
    def get_object(self):
        obj =  super().get_object()

        if self.action in ['update', 'partial_update', 'destroy'] and obj != self.request.user:
            raise PermissionDenied("You can only modify your own profile.")
        return obj


@api_view(['POST'])
@throttle_classes([PasswordResetThrottle])
def forgot_password_request(request):
    """
    INDUSTRY STANDARD: OWASP-compliant password reset request
    - Consistent response time and messages
    - Rate limiting
    - Secure token generation
    - No user enumeration
    """
    
    serializer = ForgetPasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = request.data.get('email', '').strip().lower()

    success, message, error= PasswordResetService.initiate_password_reset(email)
    
    if not success and error == "rate_limit":
        return Response(
            {"error": message},  # "Too many reset requests..."
            status=status.HTTP_429_TOO_MANY_REQUESTS
        )
    
    if not success and error:
        return Response(
            {"error": message},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return Response(
        {"message": message},
        status=status.HTTP_200_OK
    )

    

@api_view(['POST'])
def verify_reset_pin(request):
    """
    INDUSTRY STANDARD: Verify PIN and issue reset token
    - Brute force protection
    - Single-use PINs
    - Secure token exchange
    """
    email = request.data.get('email', '').strip().lower()
    pin = request.data.get('pin', '').strip()
    
    if not email or not pin or len(pin) != 6 or not pin.isdigit():
        return Response(
            {"error": "Invalid email or PIN format"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    success, message, reset_token = PasswordResetService.verify_reset_pin(email, pin)

    if not success:
        return Response(
            {"error": message, },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    return Response(
        {"message": message, "reset_token": reset_token},
        status=status.HTTP_201_CREATED
    )
    
      
@api_view(['POST'])
def reset_password(request):
    """
    INDUSTRY STANDARD: Reset password with verified token
    - Secure password validation
    - Session invalidation
    - User notification
    """
    reset_token = request.data.get('reset_token', '').strip()
    new_password = request.data.get('new_password', '')
    confirm_password = request.data.get('confirm_password', '')
    
    if not reset_token or not new_password:
        return Response(
            {"error": "Reset token and new password are required"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if new_password != confirm_password:
        return Response(
            {"error": "Passwords do not match"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Validate password strength (OWASP guidelines)
    if len(new_password) < 8:
        return Response(
            {"error": "Password must be at least 8 characters long"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    success, message = PasswordResetService.reset_password(reset_token, new_password)

    if not success:
        if "Invalid or expired reset session" in message:
            return Response(
                {"error": message},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(
            {"error": message},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    return Response(
        {"message": message},
        status=status.HTTP_200_OK
    )