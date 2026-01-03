from django.db import models


class GatewayType(models.TextChoices):
    PAYPAL = "PAYPAL", "Paypal"
    SSLCOMMERZ = "SSLCOMMERZ", "Sslcommerz"
    AMARPAY = "AMARPAY", "Amarpay"
    SHURJOPAY = "SHURJOPAY", "Shurjopay"


class PaymentStatusChoice(models.TextChoices):
    PAID = "PAID", "Paid"
    UNPAID = "UNPAID", "Unpaid"
    PENDING = "PENDING", "Payment_Pending"
    FAILED = "FAILED", "Failed"
    CANCELLED = "CANCELLED", "Cancelled"
