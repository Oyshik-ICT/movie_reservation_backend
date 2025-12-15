from payment.choice import GatewayType
from payment.models import Booking
from rest_framework import serializers


class PaymentCreateSerializer(serializers.Serializer):
    gateway_type = serializers.ChoiceField(choices=GatewayType.choices, write_only=True)
    booking = serializers.PrimaryKeyRelatedField(
        queryset=Booking.objects.all(),
        write_only=True,
        error_messages={"does_not_exist": "The specified Booking does not exist."},
    )
