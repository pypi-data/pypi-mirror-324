"""Auth HTTP BNB."""

from sincpro_payments_sdk import exceptions
from sincpro_payments_sdk.apps.qr import DataTransferObject, Feature, qr
from sincpro_payments_sdk.apps.qr.domain import QRBNBCredentials


class CommandAuthenticateBnb(DataTransferObject):
    """Authenticate BNB."""

    auth_id: str
    account_id: str


class ResponseAuthenticateBnb(QRBNBCredentials):
    """Authenticate BNB."""


@qr.feature(CommandAuthenticateBnb)
class AuthenticateBnb(Feature):
    """Authenticate BNB."""

    def execute(self, dto: CommandAuthenticateBnb) -> ResponseAuthenticateBnb:
        """Authenticate BNB."""
        credentials = QRBNBCredentials(
            account_id=dto.account_id,
            authorization_id=dto.auth_id,
        )
        curren_auth_credentials = self.bnb_auth_adapter.get_jwt(credentials)
        if not curren_auth_credentials.jwt_token:
            raise exceptions.SincproValidationError("Could not authenticate BNB account")

        qr.logger.info(
            f"Authenticated BNB account {dto.account_id} with auth_id {dto.auth_id}"
        )

        self.credential_provider.set_loader_credentials(lambda: curren_auth_credentials)
        return ResponseAuthenticateBnb.model_validate(curren_auth_credentials)
