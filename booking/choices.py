from django.db import models

class BookingStatusChoice(models.TextChoices):
        PENDING = "Pending", "Pending"
        CONFIRMED = "Confirmed", "Confirmed"
        CANCELLED = "Cancelled", "Cancelled"

class PaymentStatusChoice(models.TextChoices):
        PAID = "Paid", "Paid"
        UNPAID = "Unpaid", "Unpaid"
        PAYMENT_PENDING = "Payment Pending", "Payment Pending"