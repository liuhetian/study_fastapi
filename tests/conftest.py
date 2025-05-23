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
async def custom_test_lifespan():
    """测试用的应用生命周期管理"""
    # 创建测试数据库表
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

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
    # 替换session依赖
    app.dependency_overrides[get_session] = get_test_session
    app.dependency_overrides[get_get_session] = get_get_test_session
    client = TestClient(app)
    yield client
    
    app.dependency_overrides.clear() 