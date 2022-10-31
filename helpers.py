import logging
import requests

log = logging.getLogger(__name__)


def get_public_ip(service: str) -> str:

    return requests.get(url=f"{service}").json().get("ip")


def get_records_from_aws(client, zone_id: str, domain_name: str) -> list:
    """
    Get all records from AWS Route53

    :param client: boto3 client
    :param zone_id: AWS Route53 zone id
    :param domain_name: Domain name to get records for
    :return: list of records
    """

    record_objects = client.list_resource_record_sets(
        HostedZoneId=zone_id,
        StartRecordName=domain_name,
        StartRecordType="A",
    )

    return record_objects.get("ResourceRecordSets")


def get_records_to_update(records: list, current_public_ip: str) -> list:
    """
    Get records to update

    :param records: list of records
    :param current_public_ip: current public ip
    :return: list of changes
    """

    changes = []
    for record in records:
        if record.get("Type") != "A":
            log.info("Ignoring record %s, wrong type: %s", record.get("Name"), record.get("Type"))
            continue

        current_record_ip = record.get("ResourceRecords")[0].get("Value")
        if current_public_ip == current_record_ip:
            log.info(
                f"Current IP '{current_public_ip}' matches the IP resolved for record '{record}'. No need to update."
            )
            continue

        log.info(
            f"Current IP {current_public_ip} doesn't match record {record['Name']} IP ({current_record_ip}). Adding to batch update."
        )
        changes.append(
            {
                "Action": "UPSERT",
                "ResourceRecordSet": {
                    "Name": record["Name"],
                    "Type": "A",
                    "TTL": record["TTL"],
                    "ResourceRecords": [
                        {"Value": current_public_ip},
                    ],
                },
            }
        )

    return changes
