from django.db import models

from common.models import CommonModel


class Reservation(CommonModel):
    class ReservationKindChoices(models.TextChoices):
        BOAT = ("boat", "Boat")
        SEAPLATFORM = ("seaplatform", "Seaplatform")

    kind = models.CharField(
        max_length=15,
        choices=ReservationKindChoices.choices,
    )

    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
    )

    boat = models.ForeignKey(
        "boats.Boat",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    seaplatform = models.ForeignKey(
        "seaplatforms.Seaplatform",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    check_in = models.DateField(
        null=True,
        blank=True,
    )
    check_out = models.DateField(
        null=True,
        blank=True,
    )
    guests = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.kind.title()}: {self.user}님의 예약"
