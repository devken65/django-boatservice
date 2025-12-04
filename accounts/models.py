from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        # (DB Value, Label in admin page)
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    first_name = models.CharField(
        max_length=150,
        editable=False,
    )
    last_name = models.CharField(
        max_length=150,
        editable=False,
    )
    name = models.CharField(
        max_length=150,
        default="",
    )
    is_host = models.BooleanField(
        default=False,
    )
    photo = models.URLField(blank=True)
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
    )
