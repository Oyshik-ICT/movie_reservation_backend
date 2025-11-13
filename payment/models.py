import uuid

from booking.models import Booking
from django.db import models

from .choice import GatewayType, PaymentStatusChoice


class Payment(models.Model):
    booking = models.ForeignKey(
        Booking, on_delete=models.SET_NULL, null=True, related_name="payments"
    )
    payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    gateway_type = models.CharField(max_length=15, choices=GatewayType.choices)
    gateway_transaction_id = models.CharField(max_length=255, unique=True)
    gateway_response = models.JSONField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(
        max_length=16,
        choices=PaymentStatusChoice.choices,
        default=PaymentStatusChoice.UNPAID,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment id: {self.payment_id}, Amount: {self.amount}"
