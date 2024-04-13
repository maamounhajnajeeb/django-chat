from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from rest_framework import serializers

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "password", "first_name", "last_name", "email", )
    
    def create(self, validated_data):
        password = make_password(validated_data.pop("password"))
        validated_data.setdefault("password", password)
        print(validated_data.get("password"))
        return super().create(validated_data)
