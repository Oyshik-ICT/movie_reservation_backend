from django.db import models
from .choices import RowChoice, SeatNumberChoice, SeatTypeChoice
from movie.models import Movie

class Theater(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)

class Auditorium(models.Model):
    name = models.CharField(max_length=10)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name="auditoriums")

class Seat(models.Model):
    row_number = models.CharField(max_length=2, choices=RowChoice.choices)
    seat_number = models.IntegerField(choices=SeatNumberChoice.choices)
    seat_type = models.CharField(max_length=10, choices=SeatTypeChoice.choices)
    is_active = models.BooleanField(default=True)
    auditorium = models.ForeignKey(Auditorium, on_delete=models.CASCADE, related_name="seats")

    class Meta:
        unique_together = ('auditorium', 'row_number', 'seat_number')

class MovieShowing(models.Model):
    auditorium = models.ForeignKey(Auditorium, on_delete=models.CASCADE, related_name="movie_showing")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie_showing")
    date = models.DateField()
    time = models.TimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        unique_together = ('auditorium', 'date', 'time')
