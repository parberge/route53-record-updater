from os import environ
import logging
import requests

log = logging.getLogger(__name__)


def get_env_variable(variable: str, default_value=None) -> str:
    """
    Read environment variable
    """
    verified_variable = None
    try:
        verified_variable = environ[variable]
    except KeyError as error:
        if default_value:
            log.debug(f"No value set for {variable}, using default {default_value}")
            return default_value

        log.debug(f"Caught exception", exc_info=True)
        raise ValueError(f"Unable to read environment variable {variable}")

    return verified_variable


def get_public_ip(service: str = "https://ipconfig.io/json") -> str:

    return requests.get(url=f"{service}").json().get("ip")
