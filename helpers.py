from os import environ
import logging
import requests

log = logging.getLogger(__name__)


def get_public_ip(service: str = "https://ipconfig.io/json") -> str:

    return requests.get(url=f"{service}").json().get("ip")
