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

router = APIRouter(prefix="/history", tags=["查看历史"])

@router.get("/messages/{session_id}", response_model=list[MessageTable])
async def get_chat_history(
    session_id: str,
    session: Annotated[AsyncSession, Depends(get_session)]
):
    """
    获取聊天历史
    """
    stmt = select(MessageTable).where(MessageTable.session_id == session_id)
    res = await session.exec(stmt)
    res2 = res.all()
    return res2 


@router.get("/session/{session_id}", response_model=SessionTable)
async def get_session_history(
    session_id: str,
    session: Annotated[AsyncSession, Depends(get_session)]
):
    res = await session.get(SessionTable, session_id)
    if not res:
        raise HTTPException(status_code=404, detail="Session not found")
    logger.debug(res)

    logger.debug(res.ticket_info_pydantic)
    return res