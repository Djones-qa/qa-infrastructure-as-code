"""
UI tests for login functionality.
Tests cover happy path, error states, and edge cases.
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.ui
@pytest.mark.smoke
class TestLogin:
    """Test suite for login page functionality."""

    def test_login_page_loads(self, driver, base_url):
        """Verify the login page loads with expected elements."""
        driver.get(f"{base_url}/login")

        wait = WebDriverWait(driver, 10)
        username_field = wait.until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        password_field = driver.find_element(By.ID, "password")
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

        assert username_field.is_displayed(), "Username field should be visible"
        assert password_field.is_displayed(), "Password field should be visible"
        assert submit_button.is_displayed(), "Submit button should be visible"
        assert "Login" in driver.title, f"Expected 'Login' in title, got: {driver.title}"

    def test_successful_login(self, driver, base_url):
        """Verify a user can log in with valid credentials."""
        driver.get(f"{base_url}/login")

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(
            "testuser@example.com"
        )
        driver.find_element(By.ID, "password").send_keys("TestPassword123!")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Verify redirect to dashboard
        wait.until(EC.url_contains("/dashboard"))
        assert "/dashboard" in driver.current_url, "Should redirect to dashboard after login"

    def test_login_with_invalid_credentials(self, driver, base_url):
        """Verify appropriate error message for invalid credentials."""
        driver.get(f"{base_url}/login")

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(
            "invalid@example.com"
        )
        driver.find_element(By.ID, "password").send_keys("WrongPassword!")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        error_message = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='error-message']"))
        )
        assert error_message.is_displayed(), "Error message should be displayed"
        assert "Invalid" in error_message.text or "incorrect" in error_message.text.lower()

    def test_login_with_empty_fields(self, driver, base_url):
        """Verify validation prevents submission with empty fields."""
        driver.get(f"{base_url}/login")

        wait = WebDriverWait(driver, 10)
        submit_button = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']"))
        )
        submit_button.click()

        # Should stay on login page
        assert "/login" in driver.current_url, "Should remain on login page"

    def test_password_field_is_masked(self, driver, base_url):
        """Verify password field masks input."""
        driver.get(f"{base_url}/login")

        wait = WebDriverWait(driver, 10)
        password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))

        assert password_field.get_attribute("type") == "password", \
            "Password field should have type='password'"

    @pytest.mark.regression
    def test_login_page_title_and_meta(self, driver, base_url):
        """Verify page title and meta description for SEO."""
        driver.get(f"{base_url}/login")

        assert driver.title, "Page should have a title"
        meta_desc = driver.find_elements(By.CSS_SELECTOR, "meta[name='description']")
        assert len(meta_desc) > 0, "Page should have a meta description"
