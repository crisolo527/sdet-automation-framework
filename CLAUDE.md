# sdet-automation-framework

A hands-on Python test automation framework, built module-by-module as a learning exercise. Structured as a 6-module course covering setup, API testing, UI/E2E testing, AI agent testing, CI/CD, and reporting/polish.

**Target application:** [Automation Exercise](https://automationexercise.com) — a demo e-commerce site with both a real storefront UI and a documented REST API operating over the same underlying data (products, users, cart). This lets API-layer and UI-layer tests act on and verify the same data.

**Tech stack:** pytest, Playwright (Python), requests/httpx, Allure, GitHub Actions.

## Current module

**Module 1 — Setup: complete.** Next up: Module 2 — API testing (not started)

## Module checkpoints

**Starting a module:**
- Create the module folder (e.g. `02-api-testing/`) plus a scoped README/TODO stub inside it before writing any tests.

**Finishing a module:**
- Confirm all tests pass via `pytest`.
- Commit with message `module N complete: <name>`.
- Update the root README's module index.
- Append a short retro to `progress-log.md` (what was hard, what to revisit next time).

## Testing convention

Every module's tests must pass via `pytest` before that module is marked complete.

## Module plan

| # | Module | Scope |
|---|--------|-------|
| 1 | Setup | Repo scaffold, pytest + Playwright installed, `conftest.py` with base fixtures (API client, browser context), config layer for base URLs/env vars, one smoke test per layer (API ping + UI loads) proving the skeleton works |
| 2 | API testing | Test client wrapper around Automation Exercise's REST API (products, cart, users, auth), test data builders/factories for request payloads, assertions on status codes + response schema |
| 3 | UI/E2E | Page Object Model classes for key flows (browse → cart → checkout, login/signup), Playwright fixtures for browser/context lifecycle, tests covering the golden path plus 1-2 edge cases |
| 4 | AI agent testing | A small agent (via Claude API) that reads a page/endpoint change and generates or updates a Playwright/pytest test for it. Scoped narrowly: one target flow, not general autonomous suite maintenance |
| 5 | CI/CD | GitHub Actions workflow triggered on push/PR: install deps, run full suite, report pass/fail status. Functional but simple — no parallel matrix or flaky-retry logic for now |
| 6 | Reporting/polish | Allure report generation wired into the CI run, published to GitHub Pages; final README/polish pass across all modules |

Module 4 is intentionally the smallest, sharpest scope in the course — one agent, one flow.

## Out of scope / explicitly deferred

- No cross-repo automation or syncing logic with any other project.
- No branch-per-module workflow — sequential module folders on a single `main` branch.
- Module 4 does not attempt general autonomous test-suite maintenance — one flow only.
- CI is "functional but simple" — no parallelization, retry logic, or advanced Allure trend history for now.
