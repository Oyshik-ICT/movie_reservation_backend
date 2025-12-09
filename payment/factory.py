class PaymentGatewayFactory:
    gateways = {}

    @classmethod
    def create(cls, gateway_type, config):
        gateway_class = cls.gateways.get(gateway_type)
        return gateway_class(config)
