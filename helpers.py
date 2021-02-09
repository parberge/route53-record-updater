import logging
import requests

log = logging.getLogger(__name__)


def get_public_ip(service: str) -> str:

    return requests.get(url=f"{service}").json().get("ip")
