from django.conf import settings
from payment.choice import GatewayType
from payment.factory import PaymentGatewayFactory
from payment.models import Payment


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

        if result["status"] == "SUCCESS":
            payment.gateway_response = result
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

        payment.gateway_response = result
        payment.payment_status = "FAILED"
        payment.save(
            update_fields=[
                "gateway_response",
                "payment_status",
            ]
        )

        return {"success": False, "error": result.get("failedreason")}

    def verify_and_complete_payment(self, payment_id, callback_data):
        payment = Payment.objects.get(id=payment_id)

        result = self.gateway.verify_payment(
            transaction_id=payment.gateway_transaction_id, callback_data=callback_data
        )

        payment.gateway_response = result

        if result["success"] and result["status"] == "completed":
            payment.payment_status = "COMPLETED"
            payment.save(update_fields=["payment_status"])

            booking = payment.booking
            booking.booking_status = "CONFIRMED"
            booking.save(update_fields=["booking_status"])

            # Send confirmation email/SMS
            # self._send_confirmation(booking)

            return {
                "success": True,
                "booking_id": str(booking.booking_id),
                "payment_id": str(payment.payment_id),
            }

        payment.payment_status = "FAILED"
        payment.save(update_fields=["payment_status"])
        booking.booking_status = "CANCELLED"
        booking.save(update_fields=["booking_status"])

        return {"success": False, "error": result.get("error")}

    @classmethod
    def payment_status_update(cls, payment, status, reason=None):
        payment.payment_status = status
        payment.status_reason = reason

        payment.save(update_fields=["payment_status", "status_reason"])

    def get_geteway_config(self, gateway_type):
        if gateway_type == GatewayType.SSLCOMMERZ:
            return {
                "store_id": settings.SSLCOMMERZ_ID,
                "store_passwd": settings.SSLCOMMERZ_PASS,
                "validation_url": "https://sandbox.sslcommerz.com/validator/api/validationserverAPI.php",
            }
