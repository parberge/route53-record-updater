from helpers import get_public_ip, get_records_from_aws, get_records_to_update


class client:
    def list_resource_record_sets(self, **kwargs):
        return {"ResourceRecordSets": ["record1", "record2"]}


def test_get_public_ip(requests_mock):
    fake_service = "http://fake.com"
    fake_data = {"ip": "1.2.3.4"}
    requests_mock.get(fake_service, json=fake_data)
    assert get_public_ip(service=fake_service) == fake_data.get("ip")


def test_get_records_from_aws():
    fake_client = client()
    assert (
        len(
            get_records_from_aws(client=fake_client, zone_id="fake", domain_name="fake")
        )
        == 2
    )


def test_get_records_to_update():
    fake_records = [
        {
            "Name": "record1",
            "Type": "A",
            "TTL": 300,
            "ResourceRecords": [{"Value": "1.2.3.4"}],
        }
    ]
    test = get_records_to_update(records=fake_records, current_public_ip="1.2.3.5")

    assert len(test) == 1
    assert test[0].keys() == {"Action", "ResourceRecordSet"}
