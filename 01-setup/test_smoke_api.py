def test_products_list_returns_products(api_client):
    response = api_client.get("/productsList")
    assert response.status_code == 200
    body = response.json()
    assert "products" in body
