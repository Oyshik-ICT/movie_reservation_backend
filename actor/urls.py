from rest_framework.routers import DefaultRouter
from .views import ActorViewset

urlpatterns = []
router = DefaultRouter()
router.register("information", ActorViewset, basename="information")
urlpatterns += router.urls
