import requests
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from payment.gateways.base import BasePaymentGateway


class SslcommerzGateway(BasePaymentGateway):
    @property
    def session_url(self):
        if settings.SSLCOMMERZ_IS_SANDBOX:
            return "https://sandbox.sslcommerz.com/gwprocess/v4/api.php"
        return "https://securepay.sslcommerz.com/gwprocess/v4/api.php"

    def validate_config(self):
        if not self.config.get("store_id"):
            raise ImproperlyConfigured("store id is not found")
        if not self.config.get("store_passwd"):
            raise ImproperlyConfigured("store passwd is not found")

    def initialize_payment(
        self, payment_id, amount, currency, customer_info, meta_data=None
    ):
        BACKEND_URL = settings.BACKEND_URL
        payload = {
            "store_id": self.config["store_id"],
            "store_passwd": self.config["store_passwd"],
            "total_amount": amount,
            "currency": currency,
            "tran_id": payment_id,
            "success_url": f"{BACKEND_URL}/payments/{payment_id}/success/",
            "fail_url": f"{BACKEND_URL}/{payment_id}/failed/",
            "cancel_url": f"{BACKEND_URL}/{payment_id}/cancel/",
            "ipn_url": f"{BACKEND_URL}/payments/{payment_id}/ipn/",
            "cus_name": customer_info.get("name"),
            "cus_email": customer_info.get("email"),
            "cus_phone": customer_info.get("phone"),
            "cus_add1": "",
            "cus_city": "Dhaka",
            "cus_country": "Bangladesh",
            "shipping_method": "NO",
            "num_of_item": 1,
            "product_name": "Seat",
            "product_category": "Ticket",
            "product_profile": "general",
        }

        response = requests.post(self.session_url, data=payload)
        response.raise_for_status()

        response = response.json()
        return response
