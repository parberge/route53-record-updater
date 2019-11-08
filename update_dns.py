import os
import boto3
import requests
import logging
from helpers import get_env_variable

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())
log.setLevel(logging.INFO)

zone_id = get_env_variable(variable='AWS_ZONE_ID')
domain_name = get_env_variable(variable='AWS_DOMAIN_NAME')
aws_access_key = get_env_variable(variable='AWS_ACCESS_KEY')
aws_secret_key = get_env_variable(variable='AWS_SECRET_KEY')
public_ip_api = 'https://ipconfig.io'

current_ip = requests.get(url=f'{public_ip_api}/json').json().get('ip')
log.debug(f"Current IP: {current_ip}")

if not current_ip:
    raise ValueError("Unable to get current IP")

client = boto3.client(
    'route53',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
)

record_object = client.list_resource_record_sets(
    HostedZoneId=zone_id,
    StartRecordName=domain_name,
)

records = record_object.get('ResourceRecordSets')

ip = None
ttl = None
for item in records:
    if item.get('Type') == 'A':
        ttl = item.get('TTL')
        ip_list = item.get('ResourceRecords')
        ip = ip_list.pop().get('Value')

if not ip:
    raise ValueError(f"Unable to get IP for route 53 domain {domain_name} (zone ID {zone_id})")

if current_ip != ip:
    log.warning(f"Current IP {current_ip} doesn't match IP {ip}")

    response = client.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': domain_name,
                        'Type': 'A',
                        'TTL': ttl,
                        'ResourceRecords': [
                            {
                                'Value': current_ip
                            },
                        ],
                    }
                },
            ]
        }
    )
    log.info(response)