import pytest
from fastapi.testclient import TestClient
from app.main import app

# Create a test client using our FastAPI app
# We use a with block to ensure startup/shutdown events (like creating the logger) fire correctly
@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_query_endpoint_success(client):
    """
    Test a normal successful query.
    """
    response = client.post("/query", params={"query": "What is the capital of France?"})
    assert response.status_code == 200
    assert "Paris" in response.text

def test_query_endpoint_empty_query(client):
    """
    EDGE CASE: User sends an empty query string.
    """
    response = client.post("/query", params={"query": ""})
    assert response.status_code == 400
    assert "cannot be empty" in response.json()["detail"].lower()

def test_query_endpoint_whitespace_query(client):
    """
    EDGE CASE: User sends a query with only spaces.
    """
    response = client.post("/query", params={"query": "     "})
    assert response.status_code == 400
    assert "cannot be empty" in response.json()["detail"].lower()

def test_query_endpoint_missing_query_param(client):
    """
    EDGE CASE: User doesn't send the query parameter at all.
    """
    response = client.post("/query")
    # FastAPI automatically returns 422 Unprocessable Entity for missing required params
    assert response.status_code == 422
