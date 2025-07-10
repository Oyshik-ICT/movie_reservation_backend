from .models import Theater
from rest_framework import serializers

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