from rest_framework import serializers

from accounts.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from reviews.serializers import ReviewSerializer

from .models import Amenity, Boat


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "desc",
        )


class BoatListSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    def get_rating(self, boat):
        return boat.rating_ave()

    def get_is_owner(self, boat):
        request = self.context["request"]
        return boat.owner == request.user

    class Meta:
        model = Boat
        fields = (
            "pk",
            "name",
            "kind",
            "location",
            "price",
            "rating",
            "is_owner",
        )


class BoatDetailSerializer(serializers.ModelSerializer):
    owner = TinyUserSerializer(read_only=True)
    amenities = AmenitySerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)

    def get_rating(self, boat):
        return boat.rating_ave()

    def get_is_owner(self, boat):
        request = self.context["request"]
        return boat.owner == request.user

    class Meta:
        model = Boat
        fields = "__all__"
