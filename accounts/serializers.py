from rest_framework.serializers import ModelSerializer

from .models import User


class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "name",
            "photo",
        )


class PrivateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "password",
            "first_name",
            "last_name",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )
