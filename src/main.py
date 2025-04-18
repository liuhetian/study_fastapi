"""
聊天对话FastAPI应用入口
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8601, reload=True) 