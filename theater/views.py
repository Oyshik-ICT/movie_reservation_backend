from .models import Theater, Auditorium
from .serializers import TheaterSerializer, AuditoriumReadSerializer, AuditoriumWriteSerializer
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
    
class AuditoriumViewset(viewsets.ModelViewSet):
    queryset = Auditorium.objects.select_related("theater")
    
    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return AuditoriumReadSerializer
        
        return AuditoriumWriteSerializer
    
    def get_permissions(self):
        if self.action == "list":
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdmin]

        return super().get_permissions()
