from django.db import models

from common.models import CommonModel


class Photo(CommonModel):
    file = models.ImageField()
    desc = models.CharField(
        max_length=140,
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

    def __str__(self):
        return "Photo File"


class Video(CommonModel):
    """Only available in seaplatforms"""

    file = models.FileField()
    seaplatforms = models.OneToOneField(
        "seaplatforms.Seaplatform",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "Video File"
