from django.db import models

from common.models import CommonModel


# Create your models here.
class Boat(CommonModel):
    """Boat Model Definition"""

    class BoatKindChoices(models.TextChoices):
        CUTTLEFISH = ("cuttlefish", "Cuttlefish")
        OCTOPUS = ("octopus", "Octopus")

    name = models.CharField(max_length=10, default="")
    location = models.CharField(max_length=50, default="한국")
    people = models.IntegerField()
    kind = models.CharField(max_length=50, choices=BoatKindChoices)
    price = models.PositiveIntegerField()
    desc = models.TextField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    owner = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
    )

    amenities = models.ManyToManyField("boats.Amenity")
    category = models.ForeignKey(
        "categories.Category",
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.name


# Many to Many Relationship
class Amenity(CommonModel):
    name = models.CharField(max_length=150)
    desc = models.CharField(
        max_length=150,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Amenites"
