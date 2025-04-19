from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from .database import create_db_and_tables
from .routers import router_chat, router_debug, router_view

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    await create_db_and_tables()
    yield
    # 关闭时执行
    # 这里可以添加清理代码

app = FastAPI(
    title="聊天对话API", 
    description="基础的聊天对话FastAPI后端",
    lifespan=lifespan
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境应该设置为特定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加路由
app.include_router(router_chat.router)
app.include_router(router_debug.router)
app.include_router(router_view.router)

@app.get("/")
async def root():
    """根路径接口，返回API信息"""
    return {
        "message": "聊天对话API",
        "docs": "/docs",
    }

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理器"""
    return JSONResponse(
        status_code=500,
        content={"detail": f"发生错误: {str(exc)}"}
    ) 