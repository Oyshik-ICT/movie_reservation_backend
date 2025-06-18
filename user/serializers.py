from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.hashers import make_password

class BaseCustomSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
    
    def update(self, instance, validated_data):
        update_fields = []
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])
            
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            update_fields.append(attr)

        instance.save(update_fields=update_fields)

        return instance
    

class CustomUserSerializer(BaseCustomSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "password", "date_joined"]

        extra_kwargs = {
            "id": {"read_only": True},
            "password": {"write_only": True},
            "date_joined": {"read_only": True}
        }
    
class CustomAdminUserSerializer(BaseCustomSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "password", "role", "date_joined"]

        extra_kwargs = {
            "id": {"read_only": True},
            "password": {"write_only": True},
            "date_joined": {"read_only": True}
        }