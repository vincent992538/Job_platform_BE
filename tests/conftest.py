import pytest
import json
from django.test import Client
from django.contrib.auth.models import User
from django.core.management import call_command


@pytest.fixture(autouse=True)
def create_user(db):
    return User.objects.create_user(username="testuser", password="test123")


@pytest.fixture(autouse=True)
def load_initial_data(db):
    call_command("loaddata", "tests/data/job_data.json")


@pytest.fixture
def auth_client():
    client = Client()
    response = client.post(
        "/api/token/pair",
        data=json.dumps({
            "username": "testuser",
            "password": "test123"
        }),
        content_type="application/json"
    )
    data = response.json()
    client.defaults['HTTP_AUTHORIZATION'] = f"Bearer {data['access']}"
    return client
