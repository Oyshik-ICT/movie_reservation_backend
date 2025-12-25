from django.urls import path
from payment.views import PaymentCreateAPIView, SslcommerzIPNAPIView, SuceessAPIView

urlpatterns = [
    path("", PaymentCreateAPIView.as_view()),
    path("<uuid:payment_id>/ipn/", SslcommerzIPNAPIView.as_view()),
    path("<uuid:payment_id>/success/", SuceessAPIView.as_view()),
]
