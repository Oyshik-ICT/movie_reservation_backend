from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework.routers import DefaultRouter
from .views import UserViewset, AdminUserViewset, forgot_password_request, verify_reset_pin, reset_password


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('forget-password/', ForgetPassword, name="forget-password"),
    # path('reset-password/', ResetPassword, name="reset-password"),

    path('forgot-password/', forgot_password_request, name='forgot-password'),
    path('verify-pin/', verify_reset_pin, name='verify-pin'),
    path('reset-password/', reset_password, name='reset-password'),
]

router = DefaultRouter()
router.register("users", UserViewset, basename="users")
router.register("admin-users", AdminUserViewset, basename="adminusers")

urlpatterns += router.urls