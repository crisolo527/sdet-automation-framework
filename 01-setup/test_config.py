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
