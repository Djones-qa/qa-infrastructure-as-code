"""
API tests for health check and status endpoints.
"""
import pytest


@pytest.mark.api
@pytest.mark.smoke
class TestHealthEndpoints:
    """Test suite for health and status API endpoints."""

    def test_health_endpoint_returns_200(self, api_session, api_base_url):
        """Verify the health endpoint returns HTTP 200."""
        response = api_session.get(f"{api_base_url}/health")

        assert response.status_code == 200, \
            f"Expected 200, got {response.status_code}: {response.text}"

    def test_health_endpoint_returns_json(self, api_session, api_base_url):
        """Verify the health endpoint returns valid JSON."""
        response = api_session.get(f"{api_base_url}/health")

        assert response.headers.get("Content-Type", "").startswith("application/json"), \
            "Health endpoint should return JSON"

        data = response.json()
        assert isinstance(data, dict), "Response should be a JSON object"

    def test_health_response_has_status_field(self, api_session, api_base_url):
        """Verify the health response contains a status field."""
        response = api_session.get(f"{api_base_url}/health")
        data = response.json()

        assert "status" in data, "Health response should contain 'status' field"
        assert data["status"] in ["ok", "healthy", "up"], \
            f"Status should indicate healthy state, got: {data['status']}"

    def test_readiness_endpoint(self, api_session, api_base_url):
        """Verify the readiness endpoint indicates service is ready."""
        response = api_session.get(f"{api_base_url}/ready")

        assert response.status_code == 200, \
            f"Readiness check failed with status {response.status_code}"

    def test_version_endpoint(self, api_session, api_base_url):
        """Verify the version endpoint returns version information."""
        response = api_session.get(f"{api_base_url}/version")

        assert response.status_code == 200
        data = response.json()
        assert "version" in data, "Version endpoint should return version info"
