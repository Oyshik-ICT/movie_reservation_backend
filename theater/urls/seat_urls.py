from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views import SeatViewset

router = DefaultRouter()
router.register(r'', SeatViewset, basename='seat')

urlpatterns = router.urls