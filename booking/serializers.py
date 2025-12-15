from datetime import datetime, timedelta

from django.db import transaction
from django.db.utils import OperationalError
from django.utils import timezone
from rest_framework import serializers
from theater.models import MovieShowing, Seat
from theater.serializers import MovieShowingReadSerializer

from .models import Booking


class BuilkSeatPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def to_internal_value(self, data):
        if not hasattr(self.root, "prefetched_seats"):
            seat_ids = self.root.initial_data["seat"]

            seats = Seat.objects.filter(id__in=seat_ids)
            self.root.prefetched_seats = {str(seat.id): seat for seat in seats}

            if len(self.root.prefetched_seats) != len(seat_ids):
                raise serializers.ValidationError(f"Some seat id is not valid")

            return self.root.prefetched_seats[str(data)]

        if str(data) in self.root.prefetched_seats:
            return self.root.prefetched_seats[str(data)]

        return super().to_internal_value(data)


class BookingSerializer(serializers.ModelSerializer):
    seat = BuilkSeatPrimaryKeyRelatedField(
        queryset=Seat.objects.all(),
        many=True,
    )

    class Meta:
        model = Booking
        fields = "__all__"

        extra_kwargs = {
            "user": {"read_only": True},
            "total_money": {"read_only": True},
            "booking_id": {"read_only": True},
            "payment_id": {"read_only": True},
        }

    def validate_movie_showing(self, value):
        movieshowing_obj = value

        movie_datetime = datetime.combine(
            movieshowing_obj.date,
            movieshowing_obj.time,
        )

        movie_datetime = timezone.make_aware(movie_datetime)
        booking_deadline = movie_datetime - timedelta(minutes=30)

        if timezone.now() >= booking_deadline:
            raise serializers.ValidationError("Booking time is over for this movie")

        return value

    @transaction.atomic
    def create(self, validated_data):
        try:
            seat_ids = [seat.id for seat in validated_data["seat"]]

            if Booking.objects.filter(
                movie_showing=validated_data["movie_showing"], seat__id__in=seat_ids
            ).exists():
                raise serializers.ValidationError("Seat is booked already")

            locked_seat = list(
                Seat.objects.select_for_update()
                .select_related("auditorium__theater")
                .filter(id__in=seat_ids)
            )

            movie_auditorium, movie_theater = (
                validated_data["movie_showing"].auditorium,
                validated_data["movie_showing"].auditorium.theater,
            )
            for seat in locked_seat:
                if (
                    seat.auditorium != movie_auditorium
                    or seat.auditorium.theater != movie_theater
                ):
                    raise serializers.ValidationError(
                        "Movie showing auditorium and seat auditorium not same"
                    )
            validated_data["total_money"] = validated_data["movie_showing"].price * len(
                validated_data["seat"]
            )
            return super().create(validated_data)
        except OperationalError:
            raise serializers.ValidationError(
                "Seat is being booked by another user. Please try again."
            )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["movie_showing"] = MovieShowingReadSerializer(
            instance.movie_showing
        ).data

        return representation
