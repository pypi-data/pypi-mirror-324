"""SDK for SINCPRO SIAT SOAP API."""

from sincpro_framework import ApplicationService as _ApplicationService
from sincpro_framework import DataTransferObject
from sincpro_framework import Feature as _Feature
from sincpro_framework import UseFramework as _UseFramework

from sincpro_siat_soap.adapters.siat_exception_builder import siat_exception_builder
from sincpro_siat_soap.adapters.soap import Client, ProxySiatServices, proxy_siat
from sincpro_siat_soap.config import settings
from sincpro_siat_soap.logger import logger
from sincpro_siat_soap.shared.core_exceptions import SIATException

# ------------------------------------------------------------------------------------
# Initialize the framework
# ------------------------------------------------------------------------------------
siat_soap_sdk = _UseFramework("siat-soap-sdk", log_features=False)
siat_soap_sdk.add_dependency("proxy_siat", proxy_siat)


class DependencyContextType:
    proxy_siat: ProxySiatServices

    def soap_client(self, wsdl: str) -> Client:
        """Helper function"""
        return self.proxy_siat.siat_soap_clients.get(wsdl)

    def raise_if_transaction_is_false(self, response: dict):
        if response["transaccion"] is False:
            fn_raise_exception = siat_exception_builder(response)
            fn_raise_exception()


class Feature(_Feature, DependencyContextType):
    pass


class ApplicationService(_ApplicationService, DependencyContextType):
    pass


# ------------------------------------------------------------------------------------
# Exporting modules
# ------------------------------------------------------------------------------------

from sincpro_siat_soap.services import (
    auth_permissions,
    billing,
    digital_files,
    operations,
    synchronization_data,
)

__all__ = [
    "siat_soap_sdk",
    "auth_permissions",
    "synchronization_data",
    "Feature",
    "DataTransferObject",
]
