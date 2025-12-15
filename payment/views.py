from payment.serializers import PaymentCreateSerializer
from payment.services import PaymentService
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment_service = PaymentService(serializer.validated_data["gateway_type"])
        user = self.request.user
        payment_service.initiate_payment(
            serializer.validated_data["booking"],
            {
                "name": user.username,
                "email": user.email,
                "phone": user.phone_number,
            },
        )
        return Response({"message": "ok"})
