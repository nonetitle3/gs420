def test_health(api_client):
 r=api_client.get("/health"); assert r.status_code==200 and r.json()["status"]=="ok"
def test_root(api_client):
 r=api_client.get("/"); assert r.status_code==200 and r.json()["name"]=="GS420 AI"
def test_system_resources(api_client):
 r=api_client.get("/api/system/resources"); assert r.status_code==200 and "profile" in r.json()
def test_observability(api_client):
 r=api_client.get("/api/system/observability"); assert r.status_code==200 and "requests" in r.json()
