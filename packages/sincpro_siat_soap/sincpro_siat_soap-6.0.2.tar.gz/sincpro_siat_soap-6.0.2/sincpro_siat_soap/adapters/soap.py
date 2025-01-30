"""Module to manage the soap clients for the SIAT services"""

from typing import Dict, TypeVar

from requests import Session
from sincpro_framework.sincpro_logger import logger
from zeep import Client
from zeep.cache import InMemoryCache
from zeep.transports import Transport

# isort: off
from sincpro_siat_soap.domain import SIATEnvironment

# isort: on
from sincpro_siat_soap.config import settings
from sincpro_siat_soap.global_definitions import (
    SIAT_PRODUCTION_ENDPOINTS,
    SIAT_TESTING_ENDPOINTS,
)
from sincpro_siat_soap.shared.timeout import timeout_with_check_exists_response

WSDL_URL = TypeVar("WSDL_URL", str, None)

TMAP_CLIENT = Dict[str, Client | None]


def build_token_header(token: str) -> dict:
    header = {"apikey": f"TokenApi {token}"}
    return header


@timeout_with_check_exists_response(10)
def factory_soap_client(wsdl: str, headers: dict, cache_file_name: str) -> Client:
    cache = None
    if cache_file_name is not None:
        cache_ttl = 3600 * 8
        cache = InMemoryCache(timeout=cache_ttl)

    transport = Transport(timeout=15, cache=cache, operation_timeout=23)

    if headers:
        session = Session()
        session.headers.update(headers)
        transport.session = session

    return Client(wsdl=wsdl, transport=transport)


def factory_services(map_of_endpoints: dict, token: str) -> TMAP_CLIENT:
    """Create a dictionary of soap clients based on the map of endpoints"""
    header = build_token_header(token)

    services_dict = dict()

    for service_name, wsdl in map_of_endpoints.items():
        logger.info(f"Create/Update soap client: [{service_name}]({wsdl})")
        try:
            soap_client = factory_soap_client(
                wsdl, headers=header, cache_file_name=service_name
            )
        except Exception:
            logger.exception(f"Error creating the soap client for {service_name}")
            soap_client = None
        services_dict[service_name] = soap_client
    return services_dict


def build_siat_endpoint_map(siat_environment: SIATEnvironment) -> Dict[str, WSDL_URL]:
    """Create a map of the endpoints for the SIAT services"""
    logger.info(f"SIAT Environment: {siat_environment}")
    endpoint_hash_map = dict()

    match siat_environment:
        case SIATEnvironment.TEST:
            endpoint_hash_map = SIAT_TESTING_ENDPOINTS
        case SIATEnvironment.PRODUCTION:
            endpoint_hash_map = SIAT_PRODUCTION_ENDPOINTS

    return endpoint_hash_map


def get_siat_soap_clients_map(siat_environment: SIATEnvironment, token: str) -> TMAP_CLIENT:
    return factory_services(build_siat_endpoint_map(siat_environment), token)


class ProxySiatServices:
    """Facade to manage the SIAT services"""

    def __init__(self, siat_environment: SIATEnvironment, token: str):
        self.siat_environment = siat_environment
        self.token = token
        self.siat_services: TMAP_CLIENT = dict()
        self.setup()

    def setup(self) -> TMAP_CLIENT:
        self.siat_services = get_siat_soap_clients_map(
            self.siat_environment,
            self.token,
        )
        return self.siat_services

    def regenerate_all_soap_clients_that_are_none(self):
        """Something went wrong, regenerate all the soap clients that are None"""
        for service_name in self.siat_services.keys():
            if self.siat_services[service_name] is None:
                siat_endpoints_map = build_siat_endpoint_map(
                    self.siat_environment,
                )

                try:
                    self.siat_services[service_name] = factory_soap_client(
                        siat_endpoints_map[service_name],
                        headers=build_token_header(self.token),
                        cache_file_name=service_name,
                    )

                except Exception:
                    logger.exception(f"Error re-creating the soap client for {service_name}")
                    self.siat_services[service_name] = None

    @property
    def siat_soap_clients(self) -> TMAP_CLIENT:
        if None in self.siat_services.values():
            self.regenerate_all_soap_clients_that_are_none()
        return self.siat_services


proxy_siat = ProxySiatServices(settings.environment, settings.token)
