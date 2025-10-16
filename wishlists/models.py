from django.db import models

from common.models import CommonModel


class Wishlist(CommonModel):
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=150)
    boat = models.ManyToManyField("boats.Boat")
    seaplatform = models.ManyToManyField("seaplatforms.Seaplatform")

    def __str__(self):
        return self.name
