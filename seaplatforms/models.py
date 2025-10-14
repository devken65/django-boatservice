from django.db import models

from common.models import CommonModel


class Seaplatform(CommonModel):
    class PlatformKindChoices(models.TextChoices):
        REDFISH = ("redfish", "Redfish")
        BLUEFISH = ("bluefish", "Bluefish")

    name = models.CharField(max_length=50)
    kind = models.CharField(max_length=50, choices=PlatformKindChoices)
    location = models.CharField(max_length=100)
    desc = models.TextField()
    price = models.PositiveIntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    perks = models.ManyToManyField("seaplatforms.Perk")
    owner = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
    )


class Perk(CommonModel):
    class DetailsChoice(models.TextChoices):
        FOOD = ("food", "Food")
        TABLE = ("table", "Table")

    name = models.CharField(max_length=50)
    details = models.CharField(max_length=100, choices=DetailsChoice)
    desc = models.TextField(
        blank=True,
        default="",
    )
