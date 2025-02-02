"""Base API response wrappers."""

from abc import ABC, abstractmethod
from enum import Enum

from ..errors import (
    APIClientError,
    APIInvalidSignatureError,
    raise_for_result_code,
)
from ..signature import SignedModel, verify


class PaymentStatus(Enum):
    """Payment status."""

    INITIATED = 1
    IN_PROGRESS = 2
    CANCELLED = 3
    CONFIRMED = 4
    REVERSED = 5
    DENIED = 6
    WAITING_SETTLEMENT = 7
    SETTLED = 8
    REFUND_PROCESSING = 9
    RETURNED = 10


def get_payment_status(status: int) -> PaymentStatus:
    """Build payment status from its code."""
    try:
        return PaymentStatus(status)
    except ValueError:
        raise APIClientError(f'Unexpected paymentStatus "{status}"') from None


def _parse_result_code(response: dict) -> int:
    try:
        return int(response["resultCode"])
    except KeyError:
        raise APIClientError(
            "API response does not contain resultCode"
        ) from None
    except ValueError:
        raise APIClientError(
            f"Invalid resultCode {response['resultCode']} in response"
        ) from None


class Response(SignedModel, ABC):
    """API response."""

    def __init__(self, dttm: str, result_code: int, result_message: str):
        self.dttm = dttm
        self.result_code = result_code
        self.result_message = result_message

    @property
    def success(self) -> bool:
        """Return whether the request was successful."""
        return self.result_code == 0

    @classmethod
    def from_json(cls, response: dict, public_key: str):
        """Return response from JSON."""
        if not response:
            raise APIClientError("API returned empty response")

        result_code = _parse_result_code(response)
        raise_for_result_code(result_code, response.get("resultMessage", ""))

        obj = cls._from_json(
            response,
            response.get("dttm", ""),
            result_code,
            response.get("resultMessage", ""),
        )

        try:
            signature = response.pop("signature")
        except KeyError:
            raise APIInvalidSignatureError("Empty signature") from None

        verify(signature, obj.to_sign_text().encode(), public_key)

        return obj

    @classmethod
    @abstractmethod
    def _from_json(
        cls, response: dict, dttm: str, result_code: int, result_message: str
    ) -> "Response":
        """Return response from JSON."""
