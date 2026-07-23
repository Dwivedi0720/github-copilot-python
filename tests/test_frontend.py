def test_index_contains_ui_elements(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.data.decode('utf-8')
    assert 'id="timer"' in data
    assert 'id="dark-mode-toggle"' in data
    assert 'id="leaderboard"' in data
