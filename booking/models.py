import uuid

from django.db import models
from theater.models import MovieShowing, Seat
from user.models import CustomUser

from .choices import BookingStatusChoice, PaymentStatusChoice


class Booking(models.Model):
    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="bookings"
    )
    movie_showing = models.ForeignKey(
        MovieShowing, on_delete=models.CASCADE, related_name="movie_bookings"
    )
    seat = models.ManyToManyField(Seat, related_name="seat_booking")
    booking_status = models.CharField(
        max_length=11,
        choices=BookingStatusChoice.choices,
        default=BookingStatusChoice.PENDING,
    )
    total_money = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    payment_status = models.CharField(
        max_length=16,
        choices=PaymentStatusChoice.choices,
        default=PaymentStatusChoice.UNPAID,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            # 1. User's bookings (most common - "show my bookings")
            models.Index(fields=["user", "-created_at"]),
            # 2. Movie showing bookings (theater management)
            models.Index(fields=["movie_showing", "booking_status"]),
        ]
