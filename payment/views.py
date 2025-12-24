from payment.models import Payment
from payment.serializers import PaymentCreateSerializer
from payment.services import PaymentService
from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment_service = PaymentService(serializer.validated_data["gateway_type"])
        user = self.request.user
        data = payment_service.initiate_payment(
            serializer.validated_data["booking"],
            {
                "name": user.username,
                "email": user.email,
                "phone": user.phone_number,
            },
        )
        return Response(data)


class SslcommerzIPNAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            payment = Payment.objects.get(payment_id=kwargs["payment_id"])
        except payment.DoesNotExist:
            raise NotFound

        if request.data.get("FAILED"):
            PaymentService.payment_status_update(
                payment, "FAILED", request.data.get("error")
            )

        return Response(data="IPN received successfully")
