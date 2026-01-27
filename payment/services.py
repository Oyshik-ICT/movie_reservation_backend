from django.conf import settings
from payment.choice import GatewayType
from payment.factory import PaymentGatewayFactory
from payment.models import Payment

from .tasks import send_booking_mail


class PaymentService:
    def __init__(self, gateway_type):
        config = self.get_geteway_config(gateway_type)
        self.gateway = PaymentGatewayFactory.create(gateway_type, config)
        self.gateway_type = gateway_type

    def initiate_payment(self, booking, customer_info):
        payment = Payment.objects.create(
            booking=booking,
            gateway_type=self.gateway_type,
            amount=booking.total_money,
        )

        result = self.gateway.initialize_payment(
            payment_id=str(payment.payment_id),
            amount=payment.amount,
            currency="BDT",
            customer_info=customer_info,
        )

        payment.gateway_response = result

        if result["status"] == "SUCCESS":
            payment.payment_status = "PENDING"
            payment.save(
                update_fields=[
                    "gateway_response",
                    "payment_status",
                ]
            )

            return {
                "success": True,
                "payment_id": str(payment.payment_id),
                "payment_url": result["GatewayPageURL"],
            }

        payment.payment_status = "FAILED"
        payment.save(
            update_fields=[
                "gateway_response",
                "payment_status",
            ]
        )

        return {"success": False, "error": result.get("failedreason")}

    def verify_and_confirm_payment(self, payment, data):
        try:
            response = self.gateway.verify(data)
            self.payment_status_update(payment, "PAID")

        except Exception as e:
            self.payment_status_update(payment, "FAILED", e.args[0])

    def payment_status_update(self, payment, status, reason=None):
        payment.payment_status = status
        payment.status_reason = reason

        payment.save(update_fields=["payment_status", "status_reason"])

        if status == "PAID":
            payment.booking.confirm
            send_booking_mail.delay(
                payment.booking.user.email, payment.booking.movie_showing.movie.title
            )
        elif status in ["FAILED", "CANCELLED"]:
            payment.booking.cancel

    def get_geteway_config(self, gateway_type):
        if gateway_type == GatewayType.SSLCOMMERZ:
            return {
                "store_id": settings.SSLCOMMERZ_ID,
                "store_passwd": settings.SSLCOMMERZ_PASS,
                "validation_url": "https://sandbox.sslcommerz.com/validator/api/validationserverAPI.php",
            }
