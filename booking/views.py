from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import Booking
from .serializers import BookingSerializer


class BookingViewset(viewsets.ModelViewSet):
    queryset = Booking.objects.select_related(
        "user", "movie_showing__auditorium__theater", "movie_showing__movie"
    ).prefetch_related(
        "seat",
        "movie_showing__movie__actor",
    )

    serializer_class = BookingSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user

        if not user.is_staff:
            qs = qs.filter(user=user)

        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
