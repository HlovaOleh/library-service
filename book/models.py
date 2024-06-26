from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Book(models.Model):
    class TypeOfCovers(models.TextChoices):
        HARD = "hard", _("HARD")
        SOFT = "soft", _("SOFT")

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(
        max_length=5,
        choices=TypeOfCovers.choices,
        default=TypeOfCovers.HARD
    )
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    daily_fee = models.DecimalField(decimal_places=2, max_digits=1000)

    @property
    def available(self) -> bool:
        return bool(self.inventory)

    class Meta:
        unique_together = ("title", "author", "cover")
        ordering = ["title", "author", "-inventory"]

    def __str__(self):
        return f"{self.title} ({self.author})"
