"""
UI tests for navigation and routing.
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.ui
@pytest.mark.smoke
class TestNavigation:
    """Test suite for application navigation."""

    def test_homepage_loads(self, driver, base_url):
        """Verify the homepage loads successfully."""
        driver.get(base_url)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        assert driver.title, "Homepage should have a title"
        assert driver.current_url.rstrip("/") == base_url.rstrip("/"), \
            "Should be on the homepage"

    def test_navigation_links_present(self, driver, base_url):
        """Verify main navigation links are present."""
        driver.get(base_url)

        wait = WebDriverWait(driver, 10)
        nav = wait.until(EC.presence_of_element_located((By.TAG_NAME, "nav")))

        links = nav.find_elements(By.TAG_NAME, "a")
        assert len(links) > 0, "Navigation should contain links"

    def test_404_page(self, driver, base_url):
        """Verify 404 page is shown for unknown routes."""
        driver.get(f"{base_url}/this-page-does-not-exist-12345")

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        page_source = driver.page_source.lower()
        assert "404" in page_source or "not found" in page_source, \
            "Should display 404 or 'not found' message"

    @pytest.mark.regression
    def test_back_button_navigation(self, driver, base_url):
        """Verify browser back button works correctly."""
        driver.get(base_url)
        driver.get(f"{base_url}/login")

        driver.back()

        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_to_be(base_url + "/") if not base_url.endswith("/") else EC.url_to_be(base_url))

        assert driver.current_url.rstrip("/") == base_url.rstrip("/"), \
            "Back button should return to homepage"
