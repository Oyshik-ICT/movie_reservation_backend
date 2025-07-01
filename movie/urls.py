from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AdminMovieViewset, NormalUserMovieView

urlpatterns = [
    path("user-movies/", NormalUserMovieView, name="user-movies")
]

router = DefaultRouter()
router.register("admin-movies", AdminMovieViewset, basename="admin-movies")

urlpatterns += router.urls
