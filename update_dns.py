import boto3
import logging
from helpers import get_public_ip, get_records_from_aws, get_records_to_update
from os import environ
import socket

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())

zone_id = environ["AWS_ZONE_ID"]
domain_name = environ["AWS_DOMAIN_NAME"]
log_level = environ.get("LOG_LEVEL", "INFO")
log.setLevel(logging.getLevelName(log_level))

public_ip_service = "https://ipconfig.io/json"
current_public_ip = get_public_ip(service=public_ip_service)

if not current_public_ip:
    log.error(f"Unable to get current IP from {public_ip_service}")
    exit()
log.debug(f"Current public IP: {current_public_ip}")

domain_current_ip = socket.gethostbyname(domain_name)
if current_public_ip == domain_current_ip:
    log.info("Domain record is up to date, no need to update.")
    exit()

client = boto3.client(
    "route53",
)

records_objects = get_records_from_aws(
    client=client, zone_id=zone_id, domain_name=domain_name
)

aws_dns_records = records_objects.get("ResourceRecordSets")
log.debug("AWS Records: %s" % aws_dns_records)

changes = get_records_to_update(aws_dns_records, current_public_ip)

log.info("Apply changes...")
response = client.change_resource_record_sets(
    HostedZoneId=zone_id,
    ChangeBatch={
        "Changes": changes,
    },
)
log.info("Response from AWS: %s", response)
