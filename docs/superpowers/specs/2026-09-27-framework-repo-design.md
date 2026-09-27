# sdet-automation-framework — design spec

## Purpose

A hands-on Python test automation framework, built module-by-module as a learning exercise. Structured as a 6-module course covering setup, API testing, UI/E2E testing, AI agent testing, CI/CD, and reporting/polish. Public GitHub repo.

## Target application

**Automation Exercise** (automationexercise.com) — a demo e-commerce site with both a real storefront UI and a documented REST API operating over the same underlying data (products, users, cart). Chosen specifically so API-layer and UI-layer tests can eventually act on and verify the same data, which two disconnected demo services (e.g. a separate mock API paired with a UI-only site) cannot support.

## Tech stack

- **pytest** — test runner throughout all modules
- **Playwright (Python)** — UI/E2E automation (Module 3)
- **requests** or **httpx** — API test client (Module 2)
- **Allure** — test reporting (Module 6)
- **GitHub Actions** — CI (Module 5)

## Repo structure

Sequential module folders on a single `main` branch — no per-module branching/PR workflow, since this is a solo learning project and branch ceremony adds no value here. Later modules may extend shared fixtures/config introduced in earlier ones (e.g. Module 3's Playwright config builds on Module 1's setup).

```
sdet-automation-framework/
  README.md                    <- course overview, module index, links
  CLAUDE.md                    <- current module, workflow rules (self-contained)
  progress-log.md              <- module completion retros
  pyproject.toml / requirements.txt
  conftest.py                  <- shared fixtures (base_url, browser context, api client)
  01-setup/
  02-api-testing/
  03-ui-e2e/
  04-ai-agent-testing/
  05-ci-cd/
  06-reporting-polish/
  .github/workflows/           <- added in Module 5
```

## Module breakdown

| # | Module | Scope |
|---|--------|-------|
| 1 | Setup | Repo scaffold, pytest + Playwright installed, `conftest.py` with base fixtures (API client, browser context), config layer for base URLs/env vars, one smoke test per layer (API ping + UI loads) proving the skeleton works |
| 2 | API testing | Test client wrapper around Automation Exercise's REST API (products, cart, users, auth), test data builders/factories for request payloads, assertions on status codes + response schema |
| 3 | UI/E2E | Page Object Model classes for key flows (browse → cart → checkout, login/signup), Playwright fixtures for browser/context lifecycle, tests covering the golden path plus 1-2 edge cases |
| 4 | AI agent testing | A small agent (via Claude API) that reads a page/endpoint change and generates or updates a Playwright/pytest test for it. Scoped narrowly: one target flow, not general autonomous suite maintenance |
| 5 | CI/CD | GitHub Actions workflow triggered on push/PR: install deps, run full suite, report pass/fail status. Functional but simple — no parallel matrix or flaky-retry logic for now |
| 6 | Reporting/polish | Allure report generation wired into the CI run, published to GitHub Pages; final README/polish pass across all modules |

Module 4 is intentionally the smallest, sharpest scope in the course — one agent, one flow.

## Pacing

Session-based, no fixed cadence. Work happens whenever a framework session is chosen; there's no calendar coupling to any other project or repo.

## CLAUDE.md content plan (for this repo)

Self-contained — no references to any other repo's conventions or format.

- Purpose/context: this repo's own description (framework, module-based, target app, stack) as above.
- **Current module** line: single source of truth for where things stand, updated on module completion.
- Module checkpoints:
  - Starting a module: create the module folder plus a scoped README/TODO stub before writing any tests.
  - Finishing a module: confirm tests pass via `pytest`, commit `module N complete: <name>`, update the root README's module index, append a short retro to `progress-log.md` (what was hard, what to revisit next time).
- Testing convention: every module's tests must pass via `pytest` before it's marked complete.
- 6-module list with one-line scope for each (table above), so the plan is visible without opening other files.

## Repo setup mechanics

- **Name**: `sdet-automation-framework`
- **Visibility**: public
- **Location**: `~/Documents/Repos/sdet-automation-framework`, git-initialized locally with `main` as default branch; pushed to GitHub once initial scaffold + CLAUDE.md exist.

## Out of scope / explicitly deferred

- No cross-repo automation or syncing logic with any other project.
- No branch-per-module workflow.
- Module 4 does not attempt general autonomous test-suite maintenance — one flow only.
- CI is "functional but simple" — no parallelization, retry logic, or advanced Allure trend history for now; can be revisited later if desired.
