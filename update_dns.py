import boto3
import logging
from helpers import get_public_ip, get_records_from_aws, get_records_to_update
from os import environ
import socket

zone_id = environ["AWS_ZONE_ID"]
domain_name = environ["AWS_DOMAIN_NAME"]
log_level = environ.get("LOG_LEVEL", "INFO")

logging.basicConfig(level=logging.getLevelName(log_level))

public_ip_service = "https://ipconfig.io/json"
current_public_ip = get_public_ip(service=public_ip_service)

if not current_public_ip:
    logging.error(f"Unable to get current IP from {public_ip_service}")
    exit()
logging.info(f"Current public IP: {current_public_ip}")

domain_current_ip = socket.gethostbyname(domain_name)
if current_public_ip == domain_current_ip:
    logging.info("Domain record is up to date, no need to update.")
    exit()

client = boto3.client(
    "route53",
)

records_objects = get_records_from_aws(
    client=client, zone_id=zone_id, domain_name=domain_name
)
logging.debug(f"Records objects: {records_objects}")
changes = get_records_to_update(records=records_objects, current_public_ip=current_public_ip)
logging.debug(f"Changes: {changes}")

if not changes:
    logging.error("No changes to update. Use debug log level to see more details.")
    exit()

logging.info("Apply changes...")
response = client.change_resource_record_sets(
    HostedZoneId=zone_id,
    ChangeBatch={
        "Changes": changes,
    },
)
logging.info("Response from AWS: %s", response)
