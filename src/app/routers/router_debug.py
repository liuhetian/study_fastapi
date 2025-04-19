import pandas as pd 
from loguru import logger
from fastapi import APIRouter

from ..database import engine_debug

router = APIRouter(prefix="/debug", tags=["调试"])

@router.get("/session/{session_id}")
async def get_session_history(
    session_id: str,
    # session: Annotated[AsyncSession, Depends(get_session)]
):
    res = pd.read_sql('sessions', engine_debug)
    logger.debug(res)
    return ''