from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from .models import CustomUser
from .serializers import CustomUserSerializer, CustomAdminUserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsAdmin

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