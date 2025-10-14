from django.db import models


# Create your models here.
class CommonModel(models.Model):
    """CommonModel Definition"""

    # when created? / updated?
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return super().__str__()

    class Meta:  # noqa: DJ012
        abstract = True
