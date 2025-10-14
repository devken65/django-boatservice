from django.contrib import admin

from .models import Perk, Seaplatform


@admin.register(Seaplatform)
class SeaplatformAdmin(admin.ModelAdmin):
    pass


@admin.register(Perk)
class PerkAdmin(admin.ModelAdmin):
    pass
