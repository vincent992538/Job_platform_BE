import pytest
import json
from django.test import Client


@pytest.mark.django_db
def test_fail_login():
    client = Client()
    response = client.post(
        "/api/token/pair",
        data=json.dumps({
            "username": "testuser",
            "password": "testuser"
        }),
        content_type="application/json"
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_login_token_auth():
    """  get auth token  """
    client = Client()
    response = client.post(
        "/api/token/pair",
        data=json.dumps({
            "username": "testuser",
            "password": "test123"
        }),
        content_type="application/json"
    )
    assert response.status_code == 200
    data = response.json()
    assert "access" in data
    assert "refresh" in data
    access_token = data["access"]

    job_response = client.get("/api/jobs/", headers={
        "Authorization": f"Bearer {access_token}"
    })
    assert job_response.status_code == 200
    assert 'items' in job_response.json()


@pytest.mark.django_db
def test_protected_without_token():
    client = Client()
    response = client.get("/api/jobs/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"


@pytest.mark.django_db
def test_protected_with_invalid_token():
    client = Client()
    response = client.get("/api/jobs/", headers={
        "Authorization": "Bearer invalid.token.here"
    })
    assert response.status_code == 401
    assert "Token is invalid or expired" in str(response.json())
