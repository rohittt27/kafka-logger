
from rest_framework import serializers
from api.models import Item, User
from django.contrib.auth import authenticate


class UserLoginSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=False)
    email = serializers.EmailField()
    phone_number = serializers.CharField(required=False)
    password = serializers.CharField()
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "password",
            "access_token",
            "refresh_token",
        )

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        if not email:
            raise serializers.ValidationError("Email is required")

        if not password:
            raise serializers.ValidationError("Password is required")
        user_active = User.objects.filter(email=email).first()
        if user_active is None:
            raise serializers.ValidationError("User not found")
        if not user_active.is_active:
            raise serializers.ValidationError(
                "Your Profile is LOCK. Please connect to the support"
            )

        try:
            user = authenticate(username=email, password=password)
        except Exception:
            raise serializers.ValidationError("Error occurred while logging in")

        if not user:
            raise serializers.ValidationError("Incorrect email or password")

        if not user.is_active:
            raise serializers.ValidationError(
                "Your Profile is LOCK. Please Contact to the support"
            )

        data["user"] = user
        return {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone_number": user.phone_number,
            "access_token": user.tokens().get("access"),
            "refresh_token": user.tokens().get("refresh"),
            "password": user.password,
        }

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'