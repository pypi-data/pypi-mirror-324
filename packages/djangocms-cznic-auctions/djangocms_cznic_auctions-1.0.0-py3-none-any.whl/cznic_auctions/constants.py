from enum import Enum, unique

from django.utils.translation import gettext_lazy as _


@unique
class StatusType(Enum):
    """Auctions status."""

    new = "new"
    in_auction = "in_auction"


@unique
class SortType(Enum):
    """Auctions sort type."""

    auction_from_desc = "auction_from_desc"
    num_chars_asc = "num_chars_asc"
    price_desc = "price_desc"


STATUS_CHOICES = (
    (StatusType.new.value, _("New")),
    (StatusType.in_auction.value, _("In auction")),
)
