from typing import Tuple, Annotated
from enum import Enum

from nonebot.params import Depends
from nonebot_plugin_alconna import UniMessage
from nonebot_plugin_orm import async_scoped_session
from nonebot_plugin_session import EventSession
from sqlalchemy import select

from .client import ApiClient
from .cache import get_client
from .db import Memo, Setting


class NoMemoReason(Enum):
    NO_SETTING = 1
    NO_MEMO = 2


async def get_memo(session: EventSession, sqlSession: async_scoped_session):
    setting = await sqlSession.scalar(select(Setting).where(Setting.user_id == session.id1))
    if setting is None:
        return NoMemoReason.NO_SETTING
    memo = await sqlSession.scalar(
        select(Memo).where(Memo.id == setting.default_memo).where(Memo.user_id == session.id1)
    )
    if memo is None:
        return NoMemoReason.NO_MEMO
    return memo


MemoDependency = Annotated[Memo | NoMemoReason, Depends(get_memo)]


async def get_memo_client(session: EventSession, sqlSession: async_scoped_session, memo: MemoDependency):
    if isinstance(memo, Enum):
        return memo
    client = get_client(memo.id, memo.url, memo.token)
    return client


MemoClientDependency = Annotated[ApiClient | NoMemoReason, Depends(get_memo_client)]


async def get_memo_and_client(session: EventSession, sqlSession: async_scoped_session, memo: MemoDependency):
    if isinstance(memo, Enum):
        if memo == NoMemoReason.NO_SETTING:
            await UniMessage("请先绑定memos").finish()
        elif memo == NoMemoReason.NO_MEMO:
            await UniMessage("找不到默认memo").finish()

    client = get_client(memo.id, memo.url, memo.token)

    return memo, client


MemoAndClientDependency = Annotated[Tuple[Memo, ApiClient], Depends(get_memo_and_client)]
