from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_run(client: TestClient, sample_history):
    response = client.post(
        "/runs",
        json={
            "history": sample_history,
            "timezone": "America/New_York",
            "rangeStart": "2024-01-01T00:00:00Z",
            "rangeEnd": "2024-12-31T23:59:59Z",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "runId" in data
    assert len(data["runId"]) == 36


def test_get_insights(client: TestClient, sample_history):
    create_response = client.post(
        "/runs",
        json={
            "history": sample_history,
            "timezone": "America/New_York",
            "rangeStart": "2024-01-01T00:00:00Z",
            "rangeEnd": "2024-12-31T23:59:59Z",
        },
    )
    run_id = create_response.json()["runId"]

    response = client.get(f"/runs/{run_id}/insights")
    assert response.status_code == 200

    data = response.json()
    assert "meta" in data
    assert "totals" in data
    assert "topSites" in data
    assert "topCategories" in data
    assert "personality" in data

    assert data["meta"]["runId"] == run_id
    assert data["meta"]["timezone"] == "America/New_York"


def test_get_insights_not_found(client: TestClient):
    response = client.get("/runs/nonexistent-run-id/insights")
    assert response.status_code == 404
    assert response.json()["detail"] == "Run not found"


def test_create_run_empty_history(client: TestClient):
    response = client.post(
        "/runs",
        json={
            "history": [],
            "timezone": "UTC",
            "rangeStart": "2024-01-01T00:00:00Z",
            "rangeEnd": "2024-12-31T23:59:59Z",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "runId" in data
