from typing import Callable

from sincpro_payments_sdk.apps.cybersource.domain import CybersourceCredential
from sincpro_payments_sdk.shared.provider_credentials import CredentialProvider

TEST_MERCHANT_ID = "testrest"
TEST_KEY = "08c94330-f618-42a3-b09d-e1e43be5efda"
TEST_SECRET_KEY = "yBJxy6LjM2TmcPGu+GaJrHtkke25fPpUX+UY6/L/1tE="
TEST_PROFILE_ID = None

get_credential: Callable[[], CybersourceCredential | None] = lambda: CybersourceCredential(
    key_id=TEST_KEY,
    secret_key=TEST_SECRET_KEY,
    merchant_id=TEST_MERCHANT_ID,
    profile_id=TEST_PROFILE_ID,
)


cybersource_credential_provider: CredentialProvider[CybersourceCredential] = (
    CredentialProvider(get_credential)
)
