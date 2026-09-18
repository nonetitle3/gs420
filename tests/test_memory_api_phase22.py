def test_memory_api(api_client):
 add=api_client.post("/api/memory",json={"session_id":"phase22","kind":"fact","content":"GS420 test fact"})
 assert add.status_code in (200,201)
 search=api_client.get("/api/memory/search",params={"q":"GS420"})
 assert search.status_code==200
