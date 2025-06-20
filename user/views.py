from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from .models import CustomUser
from .serializers import CustomUserSerializer, CustomAdminUserSerializer, ForgetPasswordSerializer
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

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    reset_link = f"http://127.0.0.1:8000/auth/reset-password/?uid={uid}&token={token}"

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

