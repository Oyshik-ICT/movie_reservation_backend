from django.db import models


class BookingStatusChoice(models.TextChoices):
    PENDING = "Pending", "Pending"
    CONFIRMED = "Confirmed", "Confirmed"
    CANCELLED = "Cancelled", "Cancelled"
