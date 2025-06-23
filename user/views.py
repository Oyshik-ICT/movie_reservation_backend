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

@api_view(["POST"])  
def ForgetPassword(request):
    serializer = ForgetPasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = request.data.get("email")
    user = CustomUser.objects.get(email=email)

    custom_token = secrets.token_urlsafe(32)

    token_data = {
        "user_id": user.pk,
        "used": False
    }

    cache.set(custom_token, token_data, timeout=900)


    uid = urlsafe_base64_encode(force_bytes(user.pk))

    reset_link = f"http://127.0.0.1:8000/auth/reset-password/?uid={uid}&token={custom_token}"

    send_mail(
        subject="Reset your Password",
        message=f"Click the link to reset your password: {reset_link}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email]
    )

    return Response(
        {"details": "Password reset link send to your mail"},
        status=status.HTTP_200_OK
    )

@api_view(["POST"])
def ResetPassword(request):
    serializer = ResetPasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    uid64 = request.query_params.get("uid")
    token = request.query_params.get("token")
    new_pass = request.data.get("new_password")

    if not uid64 or not token:
        return Response(
            {"details": "Invalid Reset Link"},
            status=status.HTTP_400_BAD_REQUEST
        )

    uid = force_str(urlsafe_base64_decode(uid64))
    user = CustomUser.objects.get(pk=uid)

    if not validate_reset_token(token, user):
        return Response(
            {"details": "Invalid or Expire Reset Link"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user.set_password(new_pass)
    user.save(update_fields=["password"])

    invalid_token(token)

    return Response(
        {"details": "Password Reset Successful"},
        status=status.HTTP_400_BAD_REQUEST
    )
        

def validate_reset_token(token, user):
    token_info = cache.get(token)

    if not token_info or token_info["used"] or token_info["user_id"] != user.id:
        return False
    
    return True

def invalid_token(token):
    token_info = cache.get(token)

    if token_info:
        token_info["used"] = True
        cache.set(token, token_info, timeout=60)


