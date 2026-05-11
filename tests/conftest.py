"""
Pytest configuration and shared fixtures for the QA test suite.
"""
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webdriver import WebDriver


def pytest_addoption(parser):
    """Add custom CLI options to pytest."""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        choices=["chrome", "firefox", "edge"],
        help="Browser to run tests against (default: chrome)",
    )
    parser.addoption(
        "--env",
        action="store",
        default="local",
        choices=["local", "staging", "production"],
        help="Target environment (default: local)",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode",
    )


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "smoke: mark test as a smoke test")
    config.addinivalue_line("markers", "regression: mark test as a regression test")
    config.addinivalue_line("markers", "ui: mark test as a UI/Selenium test")
    config.addinivalue_line("markers", "api: mark test as an API test")
    config.addinivalue_line("markers", "performance: mark test as a performance test")
    config.addinivalue_line("markers", "slow: mark test as slow-running")


@pytest.fixture(scope="session")
def env(request):
    """Return the target environment."""
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def base_url(env):
    """Return the base URL for the target environment."""
    urls = {
        "local": os.getenv("LOCAL_BASE_URL", "http://localhost:8080"),
        "staging": os.getenv("STAGING_BASE_URL", "https://staging.example.com"),
        "production": os.getenv("PRODUCTION_BASE_URL", "https://app.example.com"),
    }
    return urls[env]


@pytest.fixture(scope="session")
def api_base_url(env):
    """Return the API base URL for the target environment."""
    urls = {
        "local": os.getenv("LOCAL_API_URL", "http://localhost:8080/api/v1"),
        "staging": os.getenv("STAGING_API_URL", "https://staging.example.com/api/v1"),
        "production": os.getenv("PRODUCTION_API_URL", "https://app.example.com/api/v1"),
    }
    return urls[env]


@pytest.fixture(scope="function")
def driver(request):
    """
    Provide a WebDriver instance for UI tests.
    Connects to Selenium Grid if SELENIUM_HUB_URL is set, otherwise runs locally.
    """
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    hub_url = os.getenv("SELENIUM_HUB_URL")

    web_driver = _create_driver(browser, headless, hub_url)
    web_driver.implicitly_wait(10)
    web_driver.maximize_window()

    yield web_driver

    web_driver.quit()


def _create_driver(browser: str, headless: bool, hub_url: str | None) -> WebDriver:
    """Create and return a WebDriver instance."""
    if browser == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")

        if hub_url:
            return webdriver.Remote(command_executor=f"{hub_url}/wd/hub", options=options)
        return webdriver.Chrome(options=options)

    elif browser == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")

        if hub_url:
            return webdriver.Remote(command_executor=f"{hub_url}/wd/hub", options=options)
        return webdriver.Firefox(options=options)

    else:
        raise ValueError(f"Unsupported browser: {browser}")


@pytest.fixture(scope="session")
def api_session():
    """Provide a requests Session with common headers for API tests."""
    import requests

    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json",
    })
    yield session
    session.close()
