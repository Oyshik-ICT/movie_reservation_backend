from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_booking_mail(email, movie_title):
    send_mail(
        subject=f"Booking Confirmed - {movie_title}",
        message=f"""
            Dear Customer,
            Your Booking is confirmed.

            Best regards,
            Movie Reservation Team

            """,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )

    return "Done"
