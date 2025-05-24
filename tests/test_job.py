import pytest


@pytest.mark.django_db
def test_get_job(auth_client):
    response = auth_client.get("/api/jobs/1")
    assert response.status_code == 200
    job = response.json()
    assert job['title'] == 'abc'


@pytest.mark.django_db
def test_get_not_exist_job(auth_client):
    response = auth_client.get("/api/jobs/3")
    assert response.status_code == 404


@pytest.mark.django_db
def test_create_job(auth_client):
    payload = {
        "title": "test_job",
        "description": "just a test",
        "location": "Taiwan",
        "company_name": "Testing",
        "salary_range": "10k-100k",
        "posting_date": "2025-05-24",
        "expiration_date": "2025-05-25",
        "required_skills": ["skill1", "skill2"]
    }
    response = auth_client.post(
        "/api/jobs/",
        data=payload,
        content_type="application/json"
    )
    assert response.status_code == 201


@pytest.mark.django_db
def test_create_job_missing_fields(auth_client):
    payload = {
        "description": "just a test",
        "location": "Taiwan",
        "company_name": "Testing",
        "salary_range": "10k-100k",
        "posting_date": "2025-05-24",
        "expiration_date": "2025-05-25",
        "required_skills": ["skill1", "skill2"]
    }
    response = auth_client.post(
        "/api/jobs/",
        data=payload,
        content_type="application/json"
    )
    assert response.status_code == 422


@pytest.mark.django_db
def test_create_job_worng_active_date(auth_client):
    payload = {
        "title": "test_job",
        "description": "just a test",
        "location": "Taiwan",
        "company_name": "Testing",
        "salary_range": "10k-100k",
        "posting_date": "2025-05-24",
        "expiration_date": "2025-05-23",
        "required_skills": ["skill1", "skill2"]
    }
    response = auth_client.post(
        "/api/jobs/",
        data=payload,
        content_type="application/json"
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Expriration date must be after posting date."


@pytest.mark.django_db
def test_get_jobs_list(auth_client):
    response = auth_client.get("/api/jobs/")
    assert response.status_code == 200
    job = response.json()
    assert job['total'] == 2


@pytest.mark.django_db
def test_get_jobs_list_with_location(auth_client):
    params = {
        "location": "Japan"
    }
    response = auth_client.get("/api/jobs/", query_params=params)
    assert response.status_code == 200
    job = response.json()
    assert job['total'] == 1

    params = {
        "salary_range": "30k"
    }
    response = auth_client.get("/api/jobs/", query_params=params)
    assert response.status_code == 200
    job = response.json()
    assert job['total'] == 1

    params = {
        "required_skill": "skill2"
    }
    response = auth_client.get("/api/jobs/", query_params=params)
    assert response.status_code == 200
    job = response.json()
    assert job['total'] == 1


@pytest.mark.django_db
def test_get_jobs_list_with_query(auth_client):
    """  filter job title  """
    params = {
        "query": "abc"
    }
    response = auth_client.get("/api/jobs/", query_params=params)
    assert response.status_code == 200
    job = response.json()
    assert job['total'] == 1

    """ filter both description and company   """
    params["query"] = "com2"
    response = auth_client.get("/api/jobs/", query_params=params)
    assert response.status_code == 200
    job = response.json()
    assert job['total'] == 2


@pytest.mark.django_db
def test_get_jobs_list_with_status(auth_client):
    params = {
        "status": "haha"
    }
    response = auth_client.get("/api/jobs/", query_params=params)
    assert response.status_code == 422

    params = {
        "status": "active"
    }
    response = auth_client.get("/api/jobs/", query_params=params)
    assert response.status_code == 200
    job = response.json()
    assert job['total'] == 1

    params = {
        "status": "expired"
    }
    response = auth_client.get("/api/jobs/", query_params=params)
    assert response.status_code == 200
    job = response.json()
    assert job['total'] == 0

    params = {
        "status": "scheduled"
    }
    response = auth_client.get("/api/jobs/", query_params=params)
    assert response.status_code == 200
    job = response.json()
    assert job['total'] == 1


@pytest.mark.django_db
def test_get_jobs_list_order(auth_client):
    """  order ASC  """
    params = {
        "ordering": "posting_date"
    }
    response = auth_client.get("/api/jobs/", query_params=params)
    assert response.status_code == 200
    job = response.json()
    assert job['items'][0]['id'] == 1

    """  order DESC  """
    params = {
        "ordering": "-expiration_date"
    }
    response = auth_client.get("/api/jobs/", query_params=params)
    assert response.status_code == 200
    job = response.json()
    assert job['items'][0]['id'] == 2


@pytest.mark.django_db
def test_update_job(auth_client):
    """  test update company name should be pass and no effect  """
    payload = {
        "company_name": "Testing",
    }
    response = auth_client.put(
        "/api/jobs/1",
        data=payload,
        content_type="application/json"
    )
    assert response.status_code == 200
    job = response.json()
    assert job['company_name'] != "Testing"

    payload = {
        "title": "new_title"
    }
    """  test update (not) exists job  """
    response = auth_client.put(
        "/api/jobs/4",
        data=payload,
        content_type="application/json"
    )
    assert response.status_code == 404
    response = auth_client.put(
        "/api/jobs/1",
        data=payload,
        content_type="application/json"
    )
    assert response.status_code == 200
    job = response.json()
    assert job['title'] == "new_title"


@pytest.mark.django_db
def test_update_job_active_time(auth_client):
    """  invlaid post date after old expire date  """
    payload = {
        "posting_date": "2026-05-04"
    }
    response = auth_client.put(
        "/api/jobs/1",
        data=payload,
        content_type="application/json"
    )
    assert response.status_code == 400
    """  invlaid expire date before old post date  """
    payload = {
        "expiration_date": "2024-05-04"
    }
    response = auth_client.put(
        "/api/jobs/1",
        data=payload,
        content_type="application/json"
    )
    assert response.status_code == 400
    """  invlaid post date after new expire date  """
    payload = {
        "posting_date": "2026-05-04",
        "expiration_date": "2025-06-04"
    }
    response = auth_client.put(
        "/api/jobs/1",
        data=payload,
        content_type="application/json"
    )
    assert response.status_code == 400
    """  valid post date before new expire date  """
    payload = {
        "posting_date": "2026-05-04",
        "expiration_date": "2026-06-04"
    }
    response = auth_client.put(
        "/api/jobs/1",
        data=payload,
        content_type="application/json"
    )
    assert response.status_code == 200
    job = response.json()
    assert job['posting_date'] == "2026-05-04"
    assert job['expiration_date'] == "2026-06-04"


@pytest.mark.django_db
def test_delete_job(auth_client):
    response = auth_client.delete("/api/jobs/4")
    assert response.status_code == 404

    response = auth_client.delete("/api/jobs/1")
    assert response.status_code == 204
    response = auth_client.get("/api/jobs/1")
    assert response.status_code == 404
