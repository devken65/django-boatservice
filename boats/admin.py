from django.contrib import admin

from .models import Amenity, Boat


@admin.action(description="Set all prices to 0")
def reset_prices(model_admin, request, boats):
    for boat in boats.all():
        boat.price = 0
        boat.save()


@admin.register(Boat)
class BoatAdmin(admin.ModelAdmin):
    actions = (reset_prices,)

    list_display = (
        "name",
        "kind",
        "people",
        "location",
        "price",
        "total_amenities",
        "rating_ave",
        "owner",
        "created_at",
    )

    list_filter = (
        "owner__is_host",
        "category__kind",
    )

    search_fields = (
        "name",
        "^price",
        "=people",
        "owner__username",
    )

    def total_amenities(self, boat):
        return boat.amenities.count()


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
