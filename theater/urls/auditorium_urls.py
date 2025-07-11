from rest_framework.routers import DefaultRouter
from ..views import AuditoriumViewset

urlpatterns = []

router = DefaultRouter()
router.register("auditorium-info", AuditoriumViewset, basename="auditorium-info")

urlpatterns += router.urls