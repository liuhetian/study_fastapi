from datetime import datetime, date
from typing import Literal
from sqlmodel import Field, SQLModel, Relationship
from uuid import uuid4, UUID
from enum import Enum

class SenderType(str, Enum):
    CUSTOMER = "customer"
    CUSTOMER_SERVICE = "customer service"

class BaseMessage(SQLModel):
    """聊天消息模型"""

    session_id: str = Field(index=True)
    message: str 
    sender: SenderType = SenderType.CUSTOMER_SERVICE  # 因为会手动实例化
    created_at: datetime = Field(default_factory=datetime.now)

    def __repr__(self) -> str:
        return f"Message(session_id={self.session_id}, sender={self.sender}, message={self.message[:20]}..., created_at={self.created_at})"
    
class MessageTable(BaseMessage, table=True):
    __tablename__ = "messages"
    message_id: UUID = Field(default_factory=uuid4, primary_key=True)
    send_status: int = Field(default=1)  # 0：成功 1：正在处理 2：其他问题

class ReceivedMessage(BaseMessage):
    pass 

class ReplyMessage(BaseMessage):
    message_id: UUID = Field(default_factory=uuid4, primary_key=True)
    

class SessionTable(SQLModel, table=True):
    __tablename__ = "sessions"
    session_id: str = Field(primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    
    status: str | None = Field(default=None)  # 会话状态  可能关单？

    
    # game_cd: int = Field(index=True)
    created_date: date = Field(default_factory=datetime.now, index=True)



    
    

    

