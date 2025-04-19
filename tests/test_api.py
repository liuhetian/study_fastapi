import asyncio
import pytest
import os
import sys
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator, Generator
from sqlmodel.pool import StaticPool
from contextlib import asynccontextmanager
from loguru import logger
# from asgi_lifespan import LifespanManager

# 配置loguru显示DEBUG级别日志
logger.remove()  # 移除默认处理器
logger.add(sys.stderr, level="DEBUG")  # 添加一个stderr处理器，设置级别为DEBUG

# 将项目根目录添加到sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
print(os.getcwd())
print(sys.path)

from src.app.main import app, lifespan
from src.app.database import get_session, get_get_session
from src.app.models import MessageTable, SessionTable, SenderType


# 测试数据库URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# 创建测试用的异步引擎
test_engine = create_async_engine(
    TEST_DATABASE_URL, 
    echo=False,
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool
)
mytest_async_session_maker = sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)

# 创建测试用的lifespan
# @asynccontextmanager
async def custom_test_lifespan():
    """测试用的应用生命周期管理"""
    # 创建测试数据库表
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    # yield
    # 清理测试数据库
    # async with test_engine.begin() as conn:
    #     await conn.run_sync(SQLModel.metadata.drop_all)

asyncio.run(custom_test_lifespan())

# 测试用的依赖注入替换函数
async def get_test_session() -> AsyncGenerator[AsyncSession, None]:
    """获取测试数据库会话"""

    async with mytest_async_session_maker() as session:
        yield session

def get_get_test_session() -> sessionmaker[AsyncSession]:
    return mytest_async_session_maker


@pytest.fixture(name="client")
def client_fixture():
    # 替换lifespan和session依赖
    # app: FastAPI
    app.dependency_overrides[get_session] = get_test_session
    app.dependency_overrides[get_get_session] = get_get_test_session
    # app.lifespan = custom_test_lifespan
    client = TestClient(app)
    yield client
    
    app.dependency_overrides.clear()


# 测试示例
def test_read_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200


def test_create_session(client: TestClient):
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
    # logger.debug(response.json())
    # 验证响应状态码
    assert response.status_code == 200
    
    # 验证返回的数据
    response_data = response.json()
    # logger.debug(response_data)  # 先添加 

    # 然后查询 
    response = client.get(f"/history/session/{session_id}")
    response_data = response.json()
    # logger.debug(response_data)
    assert response_data["session_id"] == session_id
    # assert response_data["status"] == session_data["status"]
    # assert response_data["ticket_info"]["user_id"] == session_data["ticket_info"]["user_id"]


def test_send_message(client: TestClient):
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
    
    
    