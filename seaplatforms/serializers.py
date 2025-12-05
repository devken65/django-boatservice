from rest_framework import serializers

from accounts.serializers import TinyUserSerializer

from .models import Perk, Seaplatform


class PerkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"


class TinyPerkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perk
        fields = (
            "name",
            "details",
            "desc",
        )


class SeaplatformListSerializer(serializers.ModelSerializer):
    owner = TinyUserSerializer(read_only=True)
    perks = TinyPerkSerializer(read_only=True, many=True)

    class Meta:
        model = Seaplatform
        fields = "__all__"


class SeaplatformDetailSerializer(serializers.ModelSerializer):
    owner = TinyUserSerializer(read_only=True)
    perks = TinyPerkSerializer(read_only=True, many=True)
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, seaplatform):
        request = self.context["request"]
        return seaplatform.owner == request.user

    class Meta:
        model = Seaplatform
        fields = "__all__"
