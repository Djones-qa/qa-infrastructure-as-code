"""
API tests for user management endpoints.
Covers CRUD operations, validation, and authentication.
"""
import pytest


@pytest.mark.api
@pytest.mark.regression
class TestUsersAPI:
    """Test suite for /users API endpoints."""

    def test_get_users_requires_auth(self, api_session, api_base_url):
        """Verify GET /users returns 401 without authentication."""
        # Remove auth header if present
        session_headers = api_session.headers.copy()
        api_session.headers.pop("Authorization", None)

        response = api_session.get(f"{api_base_url}/users")

        # Restore headers
        api_session.headers.update(session_headers)

        assert response.status_code == 401, \
            f"Expected 401 Unauthorized, got {response.status_code}"

    def test_create_user_with_valid_data(self, api_session, api_base_url):
        """Verify a user can be created with valid data."""
        payload = {
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "SecurePass123!",
            "first_name": "Test",
            "last_name": "User",
        }

        response = api_session.post(f"{api_base_url}/users", json=payload)

        assert response.status_code in [200, 201], \
            f"Expected 200/201, got {response.status_code}: {response.text}"

        data = response.json()
        assert "id" in data, "Response should contain user ID"
        assert data["email"] == payload["email"]
        assert "password" not in data, "Password should not be returned in response"

    def test_create_user_with_duplicate_email(self, api_session, api_base_url):
        """Verify duplicate email returns 409 Conflict."""
        payload = {
            "email": "duplicate@example.com",
            "username": "dupuser",
            "password": "SecurePass123!",
        }

        # Create user first time
        api_session.post(f"{api_base_url}/users", json=payload)

        # Attempt to create again with same email
        response = api_session.post(f"{api_base_url}/users", json=payload)

        assert response.status_code == 409, \
            f"Expected 409 Conflict for duplicate email, got {response.status_code}"

    def test_create_user_with_invalid_email(self, api_session, api_base_url):
        """Verify invalid email format returns 422 Unprocessable Entity."""
        payload = {
            "email": "not-a-valid-email",
            "username": "testuser",
            "password": "SecurePass123!",
        }

        response = api_session.post(f"{api_base_url}/users", json=payload)

        assert response.status_code == 422, \
            f"Expected 422 for invalid email, got {response.status_code}"

    def test_get_user_by_id(self, api_session, api_base_url):
        """Verify a user can be retrieved by ID."""
        # Create a user first
        payload = {
            "email": "getbyid@example.com",
            "username": "getbyiduser",
            "password": "SecurePass123!",
        }
        create_response = api_session.post(f"{api_base_url}/users", json=payload)

        if create_response.status_code not in [200, 201]:
            pytest.skip("Could not create test user")

        user_id = create_response.json()["id"]

        # Retrieve the user
        response = api_session.get(f"{api_base_url}/users/{user_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["email"] == payload["email"]

    def test_get_nonexistent_user_returns_404(self, api_session, api_base_url):
        """Verify 404 is returned for a non-existent user ID."""
        response = api_session.get(f"{api_base_url}/users/nonexistent-id-99999")

        assert response.status_code == 404, \
            f"Expected 404 for non-existent user, got {response.status_code}"

    def test_update_user(self, api_session, api_base_url):
        """Verify a user's details can be updated."""
        # Create a user
        payload = {
            "email": "updateme@example.com",
            "username": "updateuser",
            "password": "SecurePass123!",
            "first_name": "Original",
        }
        create_response = api_session.post(f"{api_base_url}/users", json=payload)

        if create_response.status_code not in [200, 201]:
            pytest.skip("Could not create test user")

        user_id = create_response.json()["id"]

        # Update the user
        update_payload = {"first_name": "Updated"}
        response = api_session.patch(f"{api_base_url}/users/{user_id}", json=update_payload)

        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == "Updated"

    def test_delete_user(self, api_session, api_base_url):
        """Verify a user can be deleted."""
        # Create a user
        payload = {
            "email": "deleteme@example.com",
            "username": "deleteuser",
            "password": "SecurePass123!",
        }
        create_response = api_session.post(f"{api_base_url}/users", json=payload)

        if create_response.status_code not in [200, 201]:
            pytest.skip("Could not create test user")

        user_id = create_response.json()["id"]

        # Delete the user
        delete_response = api_session.delete(f"{api_base_url}/users/{user_id}")
        assert delete_response.status_code in [200, 204]

        # Verify user is gone
        get_response = api_session.get(f"{api_base_url}/users/{user_id}")
        assert get_response.status_code == 404
