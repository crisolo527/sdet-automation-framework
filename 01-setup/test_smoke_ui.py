def test_homepage_loads(page):
    page.goto("/")
    assert "Automation Exercise" in page.title()
