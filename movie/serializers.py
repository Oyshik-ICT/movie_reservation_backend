from rest_framework import serializers
from .models import Movie

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["title", "description", "genre", "language", "actor", "poster", "release_date"]

        extra_kwargs = {"id": {"read_only": True}}