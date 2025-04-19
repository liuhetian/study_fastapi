from fastapi.testclient import TestClient
from loguru import logger

def test_create_session(client: TestClient):
    """测试创建会话"""
    # 准备测试数据
    session_data = {
        "session_id": "test_session_001",
        "status": 1,
        "ticket_info": {
            "user_id": "test_user_001"
        }
    }
    session_id = session_data["session_id"]
    
    # 发送创建会话请求
    response = client.post("/chat/new_session", json=session_data)
    
    # 验证响应状态码
    assert response.status_code == 200
    
    # 验证返回的数据
    response_data = response.json()

    # 查询会话数据
    response = client.get(f"/history/session/{session_id}")
    response_data = response.json()
    assert response_data["session_id"] == session_id 