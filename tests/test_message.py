from fastapi.testclient import TestClient
from loguru import logger

def test_send_message(client: TestClient):
    """测试发送消息"""
    # 先创建一个会话
    session_id = "test_session_002"
    session_data = {
        "session_id": session_id,
        "status": 1,
        "ticket_info": {
            "user_id": "test_user_002"
        }
    }
    client.post("/chat/new_session", json=session_data)
    
    # 准备消息数据
    message_data = {
        "session_id": session_id,
        "message": "这是一条测试消息"
    }
    
    # 发送消息请求
    response = client.post("/chat/send", json=message_data)
    
    # 验证响应状态码
    assert response.status_code == 200
    
    # 验证返回的数据
    response_data = response.json()
    logger.debug(response_data) 
    assert response_data["session_id"] == session_id

    # 查看数据
    response = client.get(f"/history/messages/{session_id}")
    response_data = response.json()
    logger.debug(response_data)
    assert response_data[0]["message"] == message_data["message"]
    assert response_data[0]["sender"] == "customer" 