import pytest
import asyncio

# 配置pytest的事件循环策略
@pytest.fixture(scope="session")
def event_loop():
    """
    创建一个更长生命周期的事件循环
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close() 