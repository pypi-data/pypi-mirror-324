"""BNB Credential providers"""

from typing import Callable

from sincpro_payments_sdk.apps.qr.domain import QRBNBCredentials
from sincpro_payments_sdk.shared.provider_credentials import CredentialProvider

get_credential: Callable[[], QRBNBCredentials | None] = lambda: QRBNBCredentials(
    account_id="test",
    authorization_id="test",
)

bnb_qr_credential_provider: CredentialProvider[QRBNBCredentials] = CredentialProvider(
    get_credential
)
