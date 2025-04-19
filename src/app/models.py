from datetime import datetime, date
from typing import Literal, Dict, Any
from sqlmodel import Field, SQLModel, Relationship, JSON
from uuid import uuid4, UUID
from enum import Enum
from pydantic import BaseModel 
from sqlmodel import Column 

class SenderType(str, Enum):
    CUSTOMER = "customer"
    CUSTOMER_SERVICE = "customer service"

class BaseMessage(SQLModel):
    """聊天消息模型"""

    session_id: str = Field(index=True)
    message: str 
    # created_at: datetime = Field(default_factory=datetime.now)

    def __repr__(self) -> str:
        return f"Message(session_id={self.session_id}, sender={self.sender}, message={self.message[:20]}..., created_at={self.created_at})"
    
class MessageTable(BaseMessage, table=True):
    __tablename__ = "messages"
    sender: SenderType = SenderType.CUSTOMER
    message_id: UUID = Field(default_factory=uuid4, primary_key=True)
    send_status: int = Field(default=1)  # 0：成功 1：正在处理 2：其他问题
    created_at: datetime = Field(default_factory=datetime.now)

class ReceivedMessage(BaseMessage):
    pass 

class ReplyMessage(BaseMessage):
    message_id: UUID = Field(default_factory=uuid4, primary_key=True)
    
# 工单信息-----------------------------------

class SessionInfo(BaseModel):
    user_id: str | None = None 

class BaseSession(SQLModel):
    session_id: str = Field(primary_key=True)
    status: int | None = Field(default=None)  # 会话状态  可能关单？
    ticket_info: dict = Field(sa_column=Column(JSON))
    # game_cd: int = Field(index=True)

    @property
    def ticket_info_pydantic(self) -> SessionInfo:
        if not hasattr(self, '_ticket_info_pydantic'):
            self._ticket_info_pydantic = SessionInfo.model_validate(self.ticket_info)
        return self._ticket_info_pydantic


class NewSession(BaseSession):
    pass 

class SessionTable(BaseSession, table=True):
    __tablename__ = "sessions"
    # 一些工单状态的储存
    created_at: datetime = Field(default_factory=datetime.now)
    created_date: date = Field(default_factory=datetime.now, index=True)

class ReplySession(SQLModel):
    session_id: str 