from django.urls import path
from payment.views import (
    CancellAPIView,
    PaymentCreateAPIView,
    PaymentListAPIView,
    SslcommerzIPNAPIView,
    SuceessAPIView,
)

urlpatterns = [
    path("", PaymentCreateAPIView.as_view()),
    path("<uuid:payment_id>/ipn/", SslcommerzIPNAPIView.as_view()),
    path("<uuid:payment_id>/success/", SuceessAPIView.as_view()),
    path("<uuid:payment_id>/failed/", CancellAPIView.as_view()),
    path("lists/", PaymentListAPIView.as_view()),
]
