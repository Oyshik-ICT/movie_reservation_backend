from django.urls import path
from payment.views import PaymentCreateAPIView

urlpatterns = [
    path("", PaymentCreateAPIView.as_view()),
]
