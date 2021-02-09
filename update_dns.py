import boto3
import logging
from helpers import get_public_ip
from os import environ
import socket

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())

zone_id = environ["AWS_ZONE_ID"]
domain_name = environ["AWS_DOMAIN_NAME"]
log_level = environ.get("LOG_LEVEL", "INFO")
log.setLevel(logging.getLevelName(log_level))

public_ip_service = "https://ipconfig.io/json"
current_ip = get_public_ip(service=public_ip_service)

if not current_ip:
    log.error(f"Unable to get current IP from {public_ip_service}")
    exit()
log.debug(f"Current IP: {current_ip}")

current_lookup_ip = socket.gethostbyname(domain_name)
log.debug(f"Current resolved IP: {current_lookup_ip}")

if current_ip == current_lookup_ip:
    log.info(
        f"Current IP got from '{public_ip_service}' matches the IP resolved for domain '{domain_name}'. No need to update."
    )
    exit()

client = boto3.client(
    "route53",
)

record_object = client.list_resource_record_sets(
    HostedZoneId=zone_id,
    StartRecordName=domain_name,
    StartRecordType="A",
    MaxItems="1",
)

records = record_object.get("ResourceRecordSets")

ip = None
ttl = None
for item in records:
    log.debug(f"Record object: {item}")
    if item.get("Type") == "A" and domain_name in item.get("Name"):
        ttl = item.get("TTL")
        ip_list = item.get("ResourceRecords")
        ip = ip_list.pop().get("Value")
        break
else:
    raise ValueError(
        f"Unable to get IP for route 53 domain {domain_name} (zone ID {zone_id})"
    )

log.info(f"Current IP {current_ip} doesn't match IP {ip}. Updating {domain_name}")

response = client.change_resource_record_sets(
    HostedZoneId=zone_id,
    ChangeBatch={
        "Changes": [
            {
                "Action": "UPSERT",
                "ResourceRecordSet": {
                    "Name": domain_name,
                    "Type": "A",
                    "TTL": ttl,
                    "ResourceRecords": [
                        {"Value": current_ip},
                    ],
                },
            },
        ]
    },
)
log.info(response)