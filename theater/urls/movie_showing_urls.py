from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views import MovieShowingViewset

router = DefaultRouter()
router.register(r'', MovieShowingViewset, basename='movie_showing')

urlpatterns = router.urls