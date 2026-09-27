import pytest
import requests
from playwright.sync_api import sync_playwright

from config import API_BASE_URL, UI_BASE_URL


class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def get(self, path, **kwargs):
        return self.session.get(f"{self.base_url}{path}", **kwargs)

    def post(self, path, **kwargs):
        return self.session.post(f"{self.base_url}{path}", **kwargs)


@pytest.fixture
def api_client():
    return ApiClient(API_BASE_URL)


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    context = browser.new_context(base_url=UI_BASE_URL)
    page = context.new_page()
    yield page
    context.close()
