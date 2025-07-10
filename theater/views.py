from .models import Theater
from .serializers import TheaterSerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from user.permissions import IsAdmin

class TheaterViewset(viewsets.ModelViewSet):
    queryset = Theater.objects.all()
    serializer_class = TheaterSerializer

    def get_permissions(self):
        if self.action == "list":
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdmin]

        return super().get_permissions()
