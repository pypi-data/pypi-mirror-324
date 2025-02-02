from faker import Faker
import pytest


@pytest.fixture(scope='session', autouse=True)
def test_fake():
    return Faker()
