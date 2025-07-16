from .models import Theater, Auditorium, Seat
from .serializers import TheaterSerializer, AuditoriumReadSerializer, AuditoriumWriteSerializer, SeatReadSerializer, SeatUpdateSerializer, SeatBulkCreateSerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from user.permissions import IsAdmin
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

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
        if self.action in ["list", "retrieve"]:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdmin]

        return super().get_permissions()
    
class SeatViewset(viewsets.ModelViewSet):
    queryset = Seat.objects.select_related("auditorium__theater")
    
    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return SeatReadSerializer
        elif self.action in ["update", "partial_update"]:
            return SeatUpdateSerializer
        
        return SeatReadSerializer
    
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdmin]

        return super().get_permissions()
    
    def create(self, request, *args, **kwargs):
        return Response(
            {"error": "Individual seat creation not allowed. Use bulk_create endpoint."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    def destroy(self, request, *args, **kwargs):
        seat = self.get_object()
        seat.is_active = False
        seat.save(update_fields=['is_active'])
        return Response(
            {"message": "Seat deactivate successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
    
    @action(detail=False, methods=['POST'], permission_classes=[IsAdmin])
    def bulk_create(self, request):
        serializer = SeatBulkCreateSerializer(data=request.data)
        if serializer.is_valid():
            seat = serializer.create(serializer.validated_data)

            return Response(
                SeatReadSerializer(seat, many=True).data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def by_auditorium(self, request):
        auditorium_id = request.query_params.get("auditorium_id")

        if not auditorium_id:
            return Response(
                {"error": "Auditorium id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not Auditorium.objects.filter(id=auditorium_id).exists():
            return Response(
                {"error": "Auditorium id is not valid"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        seats = self.get_queryset().filter(auditorium=auditorium_id)
        return Response(SeatReadSerializer(seats, many=True).data)
