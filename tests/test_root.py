from fastapi.testclient import TestClient

def test_read_root(client: TestClient):
    """测试根路由"""
    response = client.get("/")
    assert response.status_code == 200 