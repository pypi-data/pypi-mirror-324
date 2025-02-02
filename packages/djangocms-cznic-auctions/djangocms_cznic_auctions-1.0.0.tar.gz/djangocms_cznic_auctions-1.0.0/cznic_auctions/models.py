from cms.models.pluginmodel import CMSPlugin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .constants import STATUS_CHOICES


class AuctionsList(CMSPlugin):
    """Auctions list model."""

    status = models.CharField(
        verbose_name=_("Status"), max_length=50, choices=STATUS_CHOICES, default=STATUS_CHOICES[1]
    )
    size = models.PositiveSmallIntegerField(
        verbose_name=_("Table size"),
        default=10,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100),
        ],
        help_text="minimum: 1, maximum: 100",
    )

    def __str__(self):
        return f"{self.get_status_display()} {self.size}"


class Auctions(CMSPlugin):
    """Auctions model."""

    status = models.CharField(
        verbose_name=_("Status"), max_length=50, choices=STATUS_CHOICES, default=STATUS_CHOICES[1]
    )

    def __str__(self):
        return self.get_status_display()
