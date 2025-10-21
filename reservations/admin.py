from django.contrib import admin

from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "kind",
        "user",
        "boat",
        "seaplatform",
        "check_in",
        "check_out",
        "guests",
    )
    list_filter = ("kind",)
