from django.db import models

from common.models import CommonModel

RELATED_BOATS = "boats"


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
        related_name=RELATED_BOATS,
    )

    amenities = models.ManyToManyField(
        "boats.Amenity",
        related_name=RELATED_BOATS,
    )
    category = models.ForeignKey(
        "categories.Category",
        null=True,
        on_delete=models.SET_NULL,
        related_name=RELATED_BOATS,
    )

    def rating_ave(self):
        review_count = self.reviews.count()

        if review_count == 0:
            return "No Reviews"
        else:
            total_rating = 0
            for review in self.reviews.all().values("rating"):
                total_rating += review["rating"]
            return round(total_rating / review_count, 1)

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


# print("\033c",end="")
