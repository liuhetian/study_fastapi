from pathlib import Path
from typing import AsyncGenerator, List

from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

# from contextlib import asynccontextmanager
# 数据库文件路径
DB_PATH = Path("volume/dbs/chat.db")
DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"

# 创建异步引擎
engine = create_async_engine(DATABASE_URL, echo=False, future=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

from functools import wraps 

def convert_to_get_func(func):
    @wraps(func)
    def get_func():
        return func 
    return get_func 


async def create_db_and_tables():
    """创建数据库和表"""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """获取数据库会话"""
    async with async_session() as session:
        yield session

def get_get_session():
    return async_session