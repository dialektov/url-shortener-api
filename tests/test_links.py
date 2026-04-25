def test_create_and_get_stats(client):
    create_resp = client.post(
        "/links",
        json={"original_url": "https://example.com/page", "custom_alias": "hello123"},
    )
    assert create_resp.status_code == 201
    assert create_resp.json()["short_code"] == "hello123"

    stats_resp = client.get("/links/hello123/stats")
    assert stats_resp.status_code == 200
    assert stats_resp.json()["clicks"] == 0


def test_redirect_increments_clicks(client):
    client.post("/links", json={"original_url": "https://example.com/target", "custom_alias": "go12345"})
    redirect_resp = client.get("/go12345", follow_redirects=False)
    assert redirect_resp.status_code == 307
    assert redirect_resp.headers["location"] == "https://example.com/target"

    stats_resp = client.get("/links/go12345/stats")
    assert stats_resp.json()["clicks"] == 1


def test_alias_collision(client):
    client.post("/links", json={"original_url": "https://example.com/one", "custom_alias": "same"})
    second = client.post("/links", json={"original_url": "https://example.com/two", "custom_alias": "same"})
    assert second.status_code == 409
