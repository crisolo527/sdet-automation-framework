from config import UI_BASE_URL


def test_first_page_navigates(page):
    page.goto("/")
    assert page.url.startswith(UI_BASE_URL)


def test_second_page_is_independent(page):
    # A fresh page/context per test — no leftover navigation state from
    # the previous test even though `browser` is session-scoped.
    assert page.url == "about:blank"
