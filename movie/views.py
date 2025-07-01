from .models import Movie
from .serializers import MovieSerializer
from rest_framework import viewsets
from user.permissions import IsAdmin
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

class AdminMovieViewset(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    permission_classes = [IsAdmin]


@api_view(['GET'])
@permission_classes(['AllowAny'])
def NormalUserMovieView():
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)
