from rest_framework import serializers
from .models import Actor_Detail

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor_Detail
        fields = ['id', 'name']

    def update(self, instance, validated_data):
        update_fields = []

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            update_fields.append(attr)

        instance.save(update_fields=update_fields)

        return instance