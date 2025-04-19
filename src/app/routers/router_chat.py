import random
from typing import List
from loguru import logger
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker 
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select 
from ..database import get_session, get_get_session
from ..models import MessageTable, ReceivedMessage, ReplyMessage, SenderType
from ..models import NewSession, SessionTable, ReplySession
from typing import Annotated

# from src.app.schemas import ChatRequest, ChatResponse, HistoryResponse, MessageResponse

router = APIRouter(prefix="/chat", tags=["聊天"])

# 用于随机生成回复的示例短语
SAMPLE_REPLIES = [
    "我明白了，请继续。",
    "这个想法很有趣！",
    "我需要更多信息才能回答这个问题。",
    "谢谢分享，我学到了新东西。",
    "我不太确定我是否完全理解。",
    "你能详细解释一下吗？",
    "这让我想起了一个类似的情况。",
    "有道理！",
    "我需要思考一下这个问题。",
    "这是个好问题！"
]

@router.post("/send", response_model=ReplyMessage)
async def send_message(
    request: ReceivedMessage,
    get_session: Annotated[sessionmaker[AsyncSession], Depends(get_get_session)]
):
    """
    发送消息并获取回复
    """
    db_message = MessageTable.model_validate(request)
    # db_message.sender = SenderType.CUSTOMER
    
    async with get_session() as session:
        session.add(db_message)
        await session.commit()
        await session.refresh(db_message)
    received_message_id = db_message.message_id

    reply_message = random.choice(SAMPLE_REPLIES)

    async with get_session() as session:
        db_message_reply = MessageTable(
            session_id=db_message.session_id,
            message=reply_message,
            sender=SenderType.CUSTOMER_SERVICE,
            send_status=0,
        )
        db_message_received = await session.get(MessageTable, received_message_id)
        db_message_received.send_status = 0 

        session.add_all([db_message_received, db_message_reply])
        await session.commit()
        await session.refresh(db_message_reply)
        return db_message_reply
    

@router.post('/new_session', response_model=ReplySession)
async def create_new_session(
    request: NewSession,
    session: Annotated[AsyncSession, Depends(get_session)]
):
    new_session = SessionTable.model_validate(request)
    session.add(new_session)
    await session.commit()
    await session.refresh(new_session)
    return new_session
 