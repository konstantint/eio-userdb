
def test_smoke(client):
    r = client.get('/', follow_redirects=True)
    assert r.status_code == 200
    assert 'Registreerimisvorm' in r.data
