import os
from helpers import get_env_variable

def test_get_env_variable():
    os.environ["FAKE_VARIABLE"] = "fake variable"
    test = get_env_variable("FAKE_VARIABLE")
    assert isinstance(test, str)