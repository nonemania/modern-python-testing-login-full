from __future__ import annotations

import pytest
import schemathesis
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def api_schema():
    """Create schemathesis schema from the FastAPI app."""
    return schemathesis.openapi.from_asgi("/openapi.json", app)


schema = schemathesis.pytest.from_fixture("api_schema")


@schema.parametrize()
def test_api_contract(case):
    """Test API contract compliance using property-based testing with schemathesis.
    
    This test verifies that:
    - All endpoints respond according to their OpenAPI schema
    - Request/response formats match the documented API contract
    - Proper status codes are returned
    """
    with TestClient(app) as client:
        try:
            case.call_and_validate(session=client)
        except Exception as e:
            # Provide more detailed error information for debugging
            pytest.fail(f"Schemathesis test failed for {case.method} {case.formatted_path}: {e}")


# Additional test to verify specific login scenarios
@pytest.mark.parametrize("username,password,expected_status", [
    ("admin", "secret123", 200),           # Valid credentials
    ("invalid", "invalid", 401),           # Invalid credentials  
    ("", "secret123", 422),                # Empty username (validation error)
    ("admin", "", 422),                    # Empty password (validation error)
    ("admin", "x", 422),                   # Too short password (validation error)
    ("a" * 51, "secret123", 422),          # Too long username (validation error)
])
def test_login_validation(username, password, expected_status):
    """Test specific login validation scenarios explicitly."""
    with TestClient(app) as client:
        response = client.post("/api/login", json={"username": username, "password": password})
        assert response.status_code == expected_status
