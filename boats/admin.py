from django.contrib import admin

from .models import Amenity, Boat


# Register your models here.
@admin.register(Boat)
class BoatAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "kind",
        "people",
        "location",
        "price",
        "owner",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "kind",
        "location",
        "price",
        "amenities",
    )


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "desc",
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )
