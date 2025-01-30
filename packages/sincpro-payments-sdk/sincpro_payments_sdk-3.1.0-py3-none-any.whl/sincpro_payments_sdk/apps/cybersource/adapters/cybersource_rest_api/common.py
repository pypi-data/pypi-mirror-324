"""Common DTOs for CyberSource REST API."""

from sincpro_payments_sdk.apps.cybersource.domain import (
    LinkSerMMDRequired,
    PayerAuthenticationStatus,
)
from sincpro_payments_sdk.shared.client_api import ApiResponse
from sincpro_payments_sdk.shared.pydantic import BaseModel


class CyberSourceBaseResponse(ApiResponse):
    id: str


class LinkResponse(BaseModel):
    """Link response."""

    href: str
    method: str


def create_merchant_def_map(merchant_defined_data: LinkSerMMDRequired) -> list[dict]:
    """Create a map of merchant defined data."""
    format_merchant_defined_data = list()
    for key, value in merchant_defined_data.model_dump().items():
        last_word = key.split("_")[-1]
        format_merchant_defined_data.append({"key": last_word, "value": value})
    return format_merchant_defined_data


class PayerAuthenticationResponse(CyberSourceBaseResponse):
    status: PayerAuthenticationStatus
    auth_transaction_id: str
    client_ref_info: str
    cavv: str | None = None
    challenge_required: str | None = None
    access_token: str | None = None
    step_up_url: str | None = None
    token: str | None = None
