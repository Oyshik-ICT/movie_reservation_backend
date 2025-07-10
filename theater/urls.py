from rest_framework.routers import DefaultRouter
from .views import TheaterViewset

urlpatterns = []

router = DefaultRouter()
router.register("theater-info", TheaterViewset, basename="theater-info")

urlpatterns += router.urls