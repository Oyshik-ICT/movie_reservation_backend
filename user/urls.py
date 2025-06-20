from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework.routers import DefaultRouter
from .views import UserViewset, AdminUserViewset, ForgetPassword


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('forget-password/', ForgetPassword, name="forget-password")
]

routers = DefaultRouter()
routers.register("users", UserViewset, basename="users")
routers.register("admin-users", AdminUserViewset, basename="adminusers")

urlpatterns += routers.urls