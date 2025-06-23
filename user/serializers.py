from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.hashers import make_password
import re

class BaseCustomSerializer(serializers.ModelSerializer):
    def validate_password(self, value):
        if len(value) <= 6:
            raise serializers.ValidationError("Password length must be greater then 5")

        if not re.search(r'[A-Za-z]', value) or not re.search(r'[0-9]', value) or not re.search(r'[^A-Za-z0-9]', value):
            raise serializers.ValidationError("Password must contains letter, digit and special character")

        return value

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

class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        new_pass = data.get("new_password")
        confirm_pass = data.get("confirm_password")

        if new_pass != confirm_pass:
            raise serializers.ValidationError("new password and confirmed password aren't match")
        
        if len(new_pass) <= 6:
            raise serializers.ValidationError("Password length must be greater then 5")

        if not re.search(r'[A-Za-z]', new_pass) or not re.search(r'[0-9]', new_pass) or not re.search(r'[^A-Za-z0-9]', new_pass):
            raise serializers.ValidationError("Password must contains letter, digit and special character")
        
        return data