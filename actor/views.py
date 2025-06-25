from .models import Actor_Detail
from .serializers import ActorSerializer
from rest_framework import viewsets
from user.permissions import IsAdmin

class ActorViewset(viewsets.ModelViewSet):
    queryset = Actor_Detail.objects.all()
    serializer_class = ActorSerializer
    permission_classes = [IsAdmin]

