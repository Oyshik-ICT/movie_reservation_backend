from .models import Theater, Auditorium, Seat
from rest_framework import serializers
from .choices import RowChoice, SeatTypeChoice

class TheaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theater
        fields = ["id", "name", "location"]

        extra_kwargs = {"id":{"read_only": True}}

    
    def update(self, instance, validated_data):
        update_fields = []

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            update_fields.append(attr)

        instance.save(update_fields=update_fields)
        return instance

class AuditoriumWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auditorium
        fields = ["id", "name", "theater"]

        extra_kwargs = {"id":{"read_only": True}}

    def update(self, instance, validated_data):
        update_fields = []

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            update_fields.append(attr)

        instance.save(update_fields=update_fields)
        return instance

    
class AuditoriumReadSerializer(serializers.ModelSerializer):
    theater = TheaterSerializer(read_only = True)
    class Meta:
        model = Auditorium
        fields = ["id", "name", "theater"]

        extra_kwargs = {"id":{"read_only": True}}

class SeatBulkCreateSerializer(serializers.Serializer):
    auditorium_id = serializers.IntegerField()
    rows = serializers.ListField(child=serializers.CharField(max_length=1))
    seat_per_row = serializers.IntegerField()
    seat_type = serializers.CharField(max_length=10, default="regular")

    def validate(self, attrs):
        auditorium_id = attrs.get("auditorium_id")
        rows = attrs.get("rows")
        seat_per_row = attrs.get("seat_per_row")
        seat_type = attrs.get("seat_type")

        if not Auditorium.objects.filter(id=auditorium_id).exists():
            raise serializers.ValidationError("Auditorium doesn't exist")
        
        invalid_rows = [row for row in rows if row not in RowChoice.values]
        if invalid_rows:
            raise serializers.ValidationError(f"this rows {', '.join(invalid_rows)} are not valid. Use this {', '.join(RowChoice.values)}")
        
        if seat_per_row <=0 or seat_per_row > 10:
            raise serializers.ValidationError("Seat per row must be between 1 to 10")
        
        if seat_type not in SeatTypeChoice.values:
            raise serializers.ValidationError(f"Invalid seat type: {seat_type}. Use this {', '.join(SeatTypeChoice)}")

        return attrs
    
    def create(self, validated_data):
        auditorium = Auditorium.objects.get(id=validated_data["auditorium_id"])
        rows = validated_data["rows"]
        total_seat = validated_data["seat_per_row"]
        seat_type = validated_data["seat_type"]
        seats = []

        for row in rows:
            for seat_number in range(1, total_seat + 1):
                seat = Seat(
                    row_number = row, 
                    seat_number = seat_number,
                    seat_type = seat_type,
                    is_active = True,
                    auditorium = auditorium
                )

                seats.append(seat)
        
        return Seat.objects.bulk_create(seats)


class SeatReadSerializer(serializers.ModelSerializer):
    auditorium = AuditoriumReadSerializer(read_only = True)
    class Meta:
        model = Seat
        fields = ["id", "row_number", "seat_number", "seat_type", "is_active", "auditorium"]

class SeatUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ["is_active", "seat_type"]

    def update(self, instance, validated_data):
        update_fields = []

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            update_fields.append(attr)

        instance.save(update_fields=update_fields)
        return instance
