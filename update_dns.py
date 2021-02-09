import boto3
import logging
from helpers import get_public_ip
from os import environ

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())

zone_id = environ["AWS_ZONE_ID"]
domain_name = environ["AWS_DOMAIN_NAME"]
log_level = environ.get("LOG_LEVEL", "INFO")
log.setLevel(logging.getLevelName(log_level))

log.info(f"Fetching current public IP")
current_ip = get_public_ip()
if not current_ip:
    raise ValueError("Unable to get current IP")

log.info(f"Current IP: {current_ip}")

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

if current_ip != ip:
    log.info(f"Current IP {current_ip} doesn't match IP {ip}")

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
else:
    log.info(f"Current IP {current_ip} match IP {ip} from record {domain_name}")