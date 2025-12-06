from abc import ABC, abstractmethod

from django.core.exceptions import ImproperlyConfigured


class BasePaymentGateway(ABC):
    def __init__(self, config):
        self.config = config
        self.base_url = self.config.get("base_url")
        self.mode = self.config.get("mode", "sandbox")
        self.validate_config()

    def validate_config(self):
        if not self.config.get("api_key"):
            raise ImproperlyConfigured("API key is not found")
        if not self.config.get("password"):
            raise ImproperlyConfigured("Password is not found")

    def initialize_payment(
        self, payment_id, amount, currency, customer_info, meta_data=None
    ):
        pass

    def verify_payment(self, transaction_id, callback_data):
        pass

    def handle_webhook(self, webhook_data, headers):
        pass
