from rest_framework.routers import DefaultRouter
from .views import BookingViewset

urlpatterns = []
router = DefaultRouter()
router.register('', BookingViewset, basename="booking")
urlpatterns += router.urls