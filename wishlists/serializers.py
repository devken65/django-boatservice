from rest_framework.serializers import ModelSerializer

from boats.serializer import BoatListSerializer

from .models import Wishlist


class WishlistSerializer(ModelSerializer):
    boat = BoatListSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Wishlist
        fields = (
            "pk",
            "name",
            "boat",
        )
