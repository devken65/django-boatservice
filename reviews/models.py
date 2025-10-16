from django.db import models

from common.models import CommonModel


class Review(CommonModel):
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
    )
    boat = models.ForeignKey(
        "boats.Boat",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    seaplatform = models.ForeignKey(
        "seaplatforms.Seaplatform",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    desc = models.TextField()
    rating = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user}: {self.rating}"
