from django.db import models


class GatewayType(models.TextChoices):
    PAYPAL = "PAYPAL", "Paypal"
    AMARPAY = "AMARPAY", "Amarpay"
    SHURJOPAY = "SHURJOPAY", "Shurjopay"


class PaymentStatusChoice(models.TextChoices):
    PAID = "Paid", "Paid"
    UNPAID = "Unpaid", "Unpaid"
    PENDING = "PENDING", "Payment_Pending"
    FAILED = "FAILED", "Failed"
    CANCELLED = "CANCELLED", "Cancelled"
