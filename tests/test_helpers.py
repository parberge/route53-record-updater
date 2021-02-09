from helpers import get_public_ip


def test_get_public_ip(requests_mock):
    fake_service = "http://fake.com"
    fake_data = {"ip": "1.2.3.4"}
    requests_mock.get(fake_service, json=fake_data)
    assert get_public_ip(service=fake_service) == fake_data.get("ip")