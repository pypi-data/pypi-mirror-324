"""Delivery data."""

from enum import Enum
from typing import Optional


class DeliveryIndicator(Enum):
    """Delivery indicator."""

    SHIPPING = "shipping"
    SHIPPING_VERIFIED = "shipping_verified"
    INSTORE = "instore"
    DIGITAL = "digital"
    TICKET = "ticket"
    OTHER = "other"


class DeliveryMode(Enum):
    """Delivery mode."""

    ELECTRONIC = 0
    SAME_DAY = 1
    NEXT_DAY = 2
    LATER = 3


class DeliveryData:
    """Delivery data."""

    def __init__(
        self,
        indicator: Optional[DeliveryIndicator] = None,
        mode: Optional[DeliveryMode] = None,
        email: Optional[str] = None,
    ) -> None:
        self.indicator = indicator
        self.mode = mode
        self.email = email
