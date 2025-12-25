from abc import ABC, abstractmethod


class BasePaymentGateway(ABC):
    def __init__(self, config):
        self.config = config
        self.validate_config()

    @abstractmethod
    def validate_config(self):
        pass

    @abstractmethod
    def initialize_payment(
        self, payment_id, amount, currency, customer_info, meta_data=None
    ):
        pass

    @abstractmethod
    def verify(self, data):
        pass

    # @abstractmethod
    # def handle_webhook(self, webhook_data, headers):
    #     pass
