# 基础聊天对话FastAPI后端

一个简单的聊天对话FastAPI后端，支持保存消息到数据库并随机生成回复。

## 功能特点

- 使用FastAPI框架
- 使用SQLModel + aiosqlite进行数据库操作
- 保存每条消息到数据库
- 随机生成回复
- 支持获取完整对话历史

## 安装

```bash
# 克隆仓库
git clone <repo-url>
cd <repo-directory>

# 使用uv创建虚拟环境并安装依赖
uv venv
uv pip install -r requirements.txt
```

## 运行

```bash
# 从src目录运行
cd src
python main.py
```

或者

```bash
uvicorn src.app.main:app --reload
```

服务器将在 http://localhost:8000 上运行。

## API接口

### 发送消息

**POST** `/chat/send`

请求体：
```json
{
  "message": "你好，这是一条测试消息"
}
```

响应：
```json
{
  "reply": "你好！有什么我可以帮助你的吗？",
  "history": [
    {
      "id": 1,
      "content": "你好，这是一条测试消息",
      "is_user": true,
      "timestamp": "2023-04-15T12:00:00"
    },
    {
      "id": 2,
      "content": "你好！有什么我可以帮助你的吗？",
      "is_user": false,
      "timestamp": "2023-04-15T12:00:01"
    }
  ]
}
```

### 获取历史记录

**GET** `/chat/history`

响应：
```json
{
  "history": [
    {
      "id": 1,
      "content": "你好，这是一条测试消息",
      "is_user": true,
      "timestamp": "2023-04-15T12:00:00"
    },
    {
      "id": 2,
      "content": "你好！有什么我可以帮助你的吗？",
      "is_user": false,
      "timestamp": "2023-04-15T12:00:01"
    }
  ]
}
```

## API文档

访问 http://localhost:8000/docs 查看Swagger UI API文档。
