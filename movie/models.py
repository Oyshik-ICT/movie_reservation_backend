from django.db import models
from .choices import GenreChoice, LanguageChoice
from actor.models import Actor_Detail
from django.utils.text import slugify

def upload_to(instance, filename):
    clean_title = slugify(instance.title)

    return f"movies/{clean_title}/{filename}"

class Movie(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    genre = models.CharField(max_length=20, choices=GenreChoice.choices)
    language = models.CharField(max_length=15, choices=LanguageChoice.choices)
    actor = models.ManyToManyField(Actor_Detail)
    poster = models.ImageField(upload_to=upload_to)
    release_date = models.DateField()

    def __str__(self):
        return self.title
