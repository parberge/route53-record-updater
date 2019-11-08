from os import environ
import logging

log = logging.getLogger(__name__)

def get_env_variable(variable: str) -> str:
    """
    Read environment variable
    """
    verified_variable = None
    try:
        verified_variable = environ[variable]
    except KeyError as error:
        log.debug(f"Caught exception", exc_info=True)
        raise ValueError(f"Unable to read environment variable {variable}")

    return verified_variable