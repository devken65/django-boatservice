from django.utils import timezone
from rest_framework import serializers

from .models import Reservation


class CreateReservationSerializer(serializers.ModelSerializer):
    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Reservation
        fields = (
            "check_in",
            "check_out",
            "guests",
        )

    def validate_check_in(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't reservation in past")

        return value

    def validate_check_out(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't reservation in past")

        return value

    def validate(self, data):
        if data["check_out"] <= data["check_in"]:
            raise serializers.ValidationError("Check in should be smaller than check out.")

        if Reservation.objects.filter(
            check_in__lte=data["check_out"],
            check_out__gte=data["check_in"],
        ).exists():
            raise serializers.ValidationError("Some reservation already Taken")
        return data


class PublicReservationSerializer(serializers.ModelSerializer):
    place_name = serializers.SerializerMethodField()

    def get_place_name(self, place):
        if place.boat:
            return place.boat.name
        elif place.seaplatform:
            return place.seaplatform.name

    class Meta:
        model = Reservation
        fields = (
            "pk",
            "place_name",
            "check_in",
            "check_out",
            "guests",
        )
