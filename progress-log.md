# Progress log

Retros for each completed module: what was hard, what to revisit next time.

## Module 1 — Setup

What was hard: pytest doesn't put the repo root on `sys.path` just because a root-level module (`config.py`) exists — that only happens once a `conftest.py` is present. Since the config layer (Task 2) was built before the fixtures (Task 3), its tests initially failed with `ModuleNotFoundError: No module named 'config'` even though the module existed. Fixed by adding `pythonpath = ["."]` to pytest's config in `pyproject.toml`, which doesn't depend on `conftest.py` existing.

What to revisit next time: the first draft of `test_fixture_isolation.py` hardcoded the live site URL instead of importing `UI_BASE_URL` from `config.py`, which would have silently broken the env-var-override use case Task 2 was built for. Worth double-checking every new test file actually uses `config` rather than repeating literals, especially once Module 2/3 add more test files.
