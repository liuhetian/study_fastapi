from ..database import engine_debug
import pandas as pd 

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


router = APIRouter(prefix="/debug", tags=["调试"])


@router.get("/session/{session_id}")
async def get_session_history(
    session_id: str,
    # session: Annotated[AsyncSession, Depends(get_session)]
):
    res = pd.read_sql('sessions', engine_debug)
    logger.debug(res)
    return ''