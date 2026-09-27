# Module 1 — Setup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stand up the repo skeleton for sdet-automation-framework — dependencies, config layer, shared pytest/Playwright fixtures, and one smoke test per layer (API + UI) — proving the whole toolchain works end to end before any real test-writing begins in later modules.

**Architecture:** A flat root layout: `config.py` reads base URLs from env vars with sane defaults; root `conftest.py` exposes an `api_client` fixture (a thin `requests.Session` wrapper) and Playwright `browser`/`page` fixtures; `01-setup/` holds the two smoke tests that exercise both fixtures against the live Automation Exercise site. No page objects or API wrapper classes beyond this — those are Module 2/3 concerns.

**Tech Stack:** Python 3, pytest, Playwright (Python, sync API), requests.

**Spec:** `docs/superpowers/specs/2026-09-27-framework-repo-design.md`

## Global Constraints

- Sequential module folders on a single `main` branch — no per-module branching/PR workflow (spec: Repo structure).
- CLAUDE.md must stay self-contained — no references to any other repo's conventions (spec: CLAUDE.md content plan). Already created; this plan does not modify it further.
- Every module's tests must pass via `pytest` before that module is marked complete (spec: Testing convention).
- Finishing a module requires: tests pass, commit `module N complete: <name>`, update root README's module index, append retro to `progress-log.md` (spec: Module checkpoints).
- Target app is the live Automation Exercise site (automationexercise.com) — no local mock server (spec: Target application).

## Review Focus

- **Missing Playwright browser binaries:** `playwright install` not run before tests execute — the UI smoke test should fail with a clear, recognizable error rather than hanging or timing out silently. Covered by Task 4's explicit `playwright install chromium` step before running tests.
- **Live API base URL unreachable or slow:** the API smoke test should assert on a real response rather than assuming the fixture always succeeds — Task 4's test checks `status_code == 200` explicitly rather than only checking the fixture didn't raise.
- **Env var override of base URLs:** a learner (or later CI config) may need to point at a different base URL — Task 2's test verifies `config.py` honors `API_BASE_URL`/`UI_BASE_URL` env vars, not just the hardcoded defaults.
- **Fixture scope leaking state between tests:** a session-scoped `browser` shared across tests must still give each test an isolated `page`/context — Task 3's test runs two UI-fixture-consuming tests in the same file and confirms neither affects the other's page state.
- **Malformed/unexpected API response shape:** the live API could change its response shape over time — Task 4's API smoke test asserts on a specific key (`products`) in the JSON body, not just the status code, so a shape change fails loudly instead of passing vacuously.

---

## File Structure

- Create: `pyproject.toml` — project metadata, dependencies (pytest, playwright, requests), pytest config section.
- Create: `.gitignore` — venv, `__pycache__`, `.env`, Playwright artifacts.
- Create: `config.py` — root-level env-var-driven base URL config.
- Create: `conftest.py` — root-level shared fixtures: `api_client`, `browser`, `page`.
- Create: `README.md` — course overview + module index table.
- Create: `progress-log.md` — empty retro log, ready for Module 1's entry at completion.
- Create: `01-setup/README.md` — scoped stub describing Module 1's goal.
- Create: `01-setup/test_config.py` — tests for `config.py` env var behavior.
- Create: `01-setup/test_smoke_api.py` — API smoke test using `api_client`.
- Create: `01-setup/test_smoke_ui.py` — UI smoke test using `page`.

## Tasks

### Task 1: Project scaffold and dependencies

**Files:**
- Create: `pyproject.toml`
- Create: `.gitignore`
- Create: `README.md`
- Create: `progress-log.md`

**Interfaces:**
- Produces: a Python environment where `pytest` and `playwright` are installed and importable; pytest's rootdir is the repo root.

- [ ] **Step 1: Create `pyproject.toml`**

```toml
[project]
name = "sdet-automation-framework"
version = "0.1.0"
description = "Learning-sandbox test automation framework targeting Automation Exercise"
requires-python = ">=3.10"
dependencies = [
    "pytest>=8.0",
    "playwright>=1.45",
    "requests>=2.31",
]

[tool.pytest.ini_options]
testpaths = ["01-setup", "02-api-testing", "03-ui-e2e", "04-ai-agent-testing", "05-ci-cd", "06-reporting-polish"]
```

- [ ] **Step 2: Create `.gitignore`**

```
__pycache__/
*.pyc
.venv/
venv/
.env
.pytest_cache/
allure-results/
allure-report/
```

- [ ] **Step 3: Create `README.md`**

```markdown
# sdet-automation-framework

A hands-on Python test automation framework, built module-by-module as a learning exercise, targeting [Automation Exercise](https://automationexercise.com).

See [CLAUDE.md](CLAUDE.md) for the full module plan and workflow rules.

## Module index

| # | Module | Status |
|---|--------|--------|
| 1 | Setup | In progress |
| 2 | API testing | Not started |
| 3 | UI/E2E | Not started |
| 4 | AI agent testing | Not started |
| 5 | CI/CD | Not started |
| 6 | Reporting/polish | Not started |
```

- [ ] **Step 4: Create empty `progress-log.md`**

```markdown
# Progress log

Retros for each completed module: what was hard, what to revisit next time.
```

- [ ] **Step 5: Install dependencies and verify**

Run: `pip install -e .`
Expected: pytest and playwright install without error.

Run: `pytest --version`
Expected: prints a pytest version string.

- [ ] **Step 6: Commit**

```bash
git add pyproject.toml .gitignore README.md progress-log.md
git commit -m "chore: scaffold project (pyproject.toml, gitignore, README, progress log)"
```

---

### Task 2: Config layer

**Files:**
- Create: `config.py`
- Create: `01-setup/test_config.py`

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: `config.API_BASE_URL: str`, `config.UI_BASE_URL: str` — read once at import time from env vars `API_BASE_URL` / `UI_BASE_URL`, defaulting to the live Automation Exercise endpoints. Later tasks (conftest fixtures) import these two names directly.

- [ ] **Step 1: Write the failing tests**

```python
# 01-setup/test_config.py
import importlib
import os

import config


def test_default_api_base_url():
    importlib.reload(config)
    assert config.API_BASE_URL == "https://automationexercise.com/api"


def test_default_ui_base_url():
    importlib.reload(config)
    assert config.UI_BASE_URL == "https://automationexercise.com"


def test_api_base_url_env_override(monkeypatch):
    monkeypatch.setenv("API_BASE_URL", "https://example.test/api")
    importlib.reload(config)
    assert config.API_BASE_URL == "https://example.test/api"
    monkeypatch.delenv("API_BASE_URL", raising=False)
    importlib.reload(config)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest 01-setup/test_config.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'config'`

- [ ] **Step 3: Write minimal implementation**

```python
# config.py
import os

API_BASE_URL = os.environ.get("API_BASE_URL", "https://automationexercise.com/api")
UI_BASE_URL = os.environ.get("UI_BASE_URL", "https://automationexercise.com")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest 01-setup/test_config.py -v`
Expected: 3 passed

- [ ] **Step 5: Commit**

```bash
git add config.py 01-setup/test_config.py
git commit -m "feat: add env-var-driven base URL config"
```

---

### Task 3: Shared fixtures (`conftest.py`)

**Files:**
- Create: `conftest.py`
- Create: `01-setup/README.md`

**Interfaces:**
- Consumes: `config.API_BASE_URL`, `config.UI_BASE_URL` (Task 2).
- Produces:
  - `api_client` fixture (function-scoped) — yields an `ApiClient` instance with `.get(path, **kwargs)` / `.post(path, **kwargs)` methods that prefix `path` with `API_BASE_URL` and return a `requests.Response`.
  - `browser` fixture (session-scoped) — yields a Playwright `Browser` instance (chromium).
  - `page` fixture (function-scoped) — yields a Playwright `Page` with `base_url` set to `config.UI_BASE_URL`, so tests can call `page.goto("/")` with relative paths.

- [ ] **Step 1: Write the failing fixture isolation test**

```python
# 01-setup/test_fixture_isolation.py
def test_first_page_navigates(page):
    page.goto("/")
    assert page.url.startswith("https://automationexercise.com")


def test_second_page_is_independent(page):
    # A fresh page/context per test — no leftover navigation state from
    # the previous test even though `browser` is session-scoped.
    assert page.url == "about:blank"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest 01-setup/test_fixture_isolation.py -v`
Expected: FAIL with `fixture 'page' not found`

- [ ] **Step 3: Write `conftest.py`**

```python
# conftest.py
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
```

- [ ] **Step 4: Write `01-setup/README.md` stub**

```markdown
# Module 1 — Setup

Goal: prove the toolchain end to end — pytest, Playwright, and the API client fixture all work against the live Automation Exercise site.

- `test_config.py` — config layer env var behavior
- `test_fixture_isolation.py` — page fixture isolation between tests
- `test_smoke_api.py` — API layer ping
- `test_smoke_ui.py` — UI layer loads
```

- [ ] **Step 5: Install Playwright browser binaries**

Run: `playwright install chromium`
Expected: downloads the chromium binary without error.

- [ ] **Step 6: Run tests to verify they pass**

Run: `pytest 01-setup/test_fixture_isolation.py -v`
Expected: 2 passed

- [ ] **Step 7: Commit**

```bash
git add conftest.py 01-setup/README.md 01-setup/test_fixture_isolation.py
git commit -m "feat: add shared api_client/browser/page fixtures"
```

---

### Task 4: Module 1 smoke tests

**Files:**
- Create: `01-setup/test_smoke_api.py`
- Create: `01-setup/test_smoke_ui.py`
- Modify: `README.md` (module index status)
- Modify: `progress-log.md` (Module 1 retro)

**Interfaces:**
- Consumes: `api_client` fixture and `page` fixture (Task 3).
- Produces: nothing consumed by later tasks — this is the module's terminal deliverable.

- [ ] **Step 1: Write the failing API smoke test**

```python
# 01-setup/test_smoke_api.py
def test_products_list_returns_products(api_client):
    response = api_client.get("/productsList")
    assert response.status_code == 200
    body = response.json()
    assert "products" in body
```

- [ ] **Step 2: Run test to verify current state**

Run: `pytest 01-setup/test_smoke_api.py -v`
Expected: PASS (fixture already exists from Task 3; this step confirms the live API responds as expected before treating it as done).

- [ ] **Step 3: Write the failing UI smoke test**

```python
# 01-setup/test_smoke_ui.py
def test_homepage_loads(page):
    page.goto("/")
    assert "Automation Exercise" in page.title()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest 01-setup/test_smoke_ui.py -v`
Expected: PASS

- [ ] **Step 5: Run the full Module 1 suite**

Run: `pytest 01-setup/ -v`
Expected: all tests pass (`test_config.py`, `test_fixture_isolation.py`, `test_smoke_api.py`, `test_smoke_ui.py`).

- [ ] **Step 6: Update `README.md` module index**

Change the Module 1 row's status from `In progress` to `Complete`.

- [ ] **Step 7: Append retro to `progress-log.md`**

Append a `## Module 1 — Setup` section with two lines, "What was hard:" and "What to revisit next time:", written from what actually happened while doing Tasks 1-4 (e.g. env var reload quirks in Task 2's tests, Playwright binary install in Task 3) — not template text.

- [ ] **Step 8: Commit**

```bash
git add 01-setup/test_smoke_api.py 01-setup/test_smoke_ui.py README.md progress-log.md
git commit -m "module 1 complete: setup"
```
