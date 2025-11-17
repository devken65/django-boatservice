from rest_framework.serializers import ModelSerializer

from accounts.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer

from .models import Amenity, Boat


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "desc",
        )


class BoatListSerializer(ModelSerializer):
    class Meta:
        model = Boat
        fields = (
            "pk",
            "name",
            "kind",
            "location",
            "price",
        )


class BoatDetailSerializer(ModelSerializer):
    owner = TinyUserSerializer(read_only=True)
    amenities = AmenitySerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Boat
        fields = "__all__"
