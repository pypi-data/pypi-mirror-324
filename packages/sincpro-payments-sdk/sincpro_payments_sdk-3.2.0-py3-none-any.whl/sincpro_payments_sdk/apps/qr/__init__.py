"""Framework for QR code generation and payment processing."""

from sincpro_framework import ApplicationService as _ApplicationService
from sincpro_framework import DataTransferObject
from sincpro_framework import Feature as _Feature
from sincpro_framework import UseFramework as _UseFramework

from sincpro_payments_sdk.apps.qr.adapters import bnb_auth_adapter, bnb_qr_adapter
from sincpro_payments_sdk.apps.qr.infrastructure.bnb.bnb_loader_credentials import (
    QRBNBCredentials,
    bnb_qr_credential_provider,
)
from sincpro_payments_sdk.shared.provider_credentials import CredentialProvider


class DependencyContextType:
    """Typing helper."""

    credential_provider: CredentialProvider[QRBNBCredentials]
    bnb_auth_adapter: bnb_auth_adapter.BNBAuthAdapter
    bnb_qr_adapter: bnb_qr_adapter.QRBNBApiAdapter


qr = _UseFramework("payment-qr")
qr.add_dependency("credential_provider", bnb_qr_credential_provider)
qr.add_dependency("bnb_auth_adapter", bnb_auth_adapter.BNBAuthAdapter())
qr.add_dependency("bnb_qr_adapter", bnb_qr_adapter.QRBNBApiAdapter())


class Feature(_Feature, DependencyContextType):
    pass


class ApplicationService(_ApplicationService, DependencyContextType):
    pass


from .use_cases import bnb

__all__ = [
    "qr",
    "bnb",
    "Feature",
    "ApplicationService",
    "DataTransferObject",
]
