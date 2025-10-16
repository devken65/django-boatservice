from django.db import models

from common.models import CommonModel


# Create your models here.
class Category(CommonModel):
    class CategoryKindChoices(models.TextChoices):
        BOATS = ("boat", "Boat")
        SEAPLATFORMS = ("seaplatform", "Seaplatform")

    name = models.CharField(max_length=50)
    kind = models.CharField(
        max_length=15,
        choices=CategoryKindChoices,
    )

    def __str__(self):
        return f"{self.name}: {self.kind}"

    class Meta:
        verbose_name_plural = "Categories"
