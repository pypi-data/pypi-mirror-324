from json import loads
from typing import Any

from nonebot import logger, require

require("nonebot_plugin_alconna")
require("nonebot_plugin_orm")
require("nonebot_plugin_session")
require("nonebot_plugin_session_orm")

from nonebot.plugin import PluginMetadata
from nonebot.plugin import inherit_supported_adapters
from sqlalchemy import or_, select

from .config import Config
from .db import Memo, MemoRecord, Setting
from .client import ApiClient
from .depend import MemoAndClientDependency
from .util import get_image_bytes

from nonebot_plugin_session_orm import get_session_persist_id
from nonebot_plugin_alconna import Image, Match, MsgId, UniMessage, UniMsg, on_alconna
from nonebot_plugin_alconna.builtins.extensions import ReplyRecordExtension
from arclet.alconna import Alconna, Arg, Args, Namespace, Option, Subcommand, namespace, StrMulti
from nonebot_plugin_session import EventSession
from nonebot_plugin_orm import async_scoped_session

__plugin_metadata__ = PluginMetadata(
    name="memos",
    description="plugin for memos",
    usage="memos help",
    type="application",
    homepage="https://github.com/eya46/nonebot_plugin_memos",
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna", "nonebot_plugin_session"),
    config=Config,
)

with namespace(Namespace("memos", strict=False)) as ns:
    memos = on_alconna(
        Alconna(
            "memos",
            Subcommand("bind", Args["url", str]["token", str]),
            Subcommand("list"),
            Subcommand("default", Arg("memo_id", int)),
            Subcommand("unbind", Arg("memo_id", int)),
            Subcommand("create", Arg("content?", StrMulti, seps="\n")),
            Subcommand("comment", Option("--uid|-u", Arg("uid?", str)), Arg("content", StrMulti, seps="\n")),
            Subcommand("link", Arg("uid?", str)),
            namespace=Namespace("memos", strict=False),
        ),
        extensions=[ReplyRecordExtension()],
    )


@memos.assign("bind")
async def bind_handler(
    url: Match[str],
    token: Match[str],
    session: EventSession,
    sqlSession: async_scoped_session,
):
    if session.level != 1:
        await UniMessage("请在私聊中使用此命令").finish()

    user_info = "null"

    try:
        client = ApiClient(url.result, token.result)
        resp = await client.getAuthStatus()
        if resp.status_code != 200:
            return await UniMessage("memos身份校验失败!").send()
        user_info = resp.text
    except Exception as e:
        await UniMessage(f"检查memos服务失败: {e}").finish()

    session_persist_id = await get_session_persist_id(session)

    memo = await sqlSession.scalar(
        select(Memo).where(Memo.user_id == session.id1).where(Memo.session_persist_id == session_persist_id)
    )

    setting = await sqlSession.scalar(select(Setting).where(Setting.user_id == session.id1))

    if memo:
        memo.url = url.result
        memo.token = token.result
        memo.user_info = user_info
        sqlSession.add(memo)
        await UniMessage("更新绑定成功!").send()
    else:
        memo = Memo(
            user_id=session.id1,
            user_info=user_info,
            session_persist_id=session_persist_id,
            url=url.result,
            token=token.result,
        )
        sqlSession.add(memo)
        await sqlSession.flush()
        await UniMessage("绑定成功").send()

    if setting is None:  # 如果没有设置默认memo
        setting = Setting(user_id=session.id1, default_memo=memo.id)
        sqlSession.add(setting)

    await sqlSession.commit()


@memos.assign("list")
async def list_handler(session: EventSession, sqlSession: async_scoped_session):
    memos = await sqlSession.scalars(select(Memo).where(Memo.user_id == session.id1))

    memos = memos.all()

    if len(memos) == 0:
        await UniMessage("未绑定任何memos").finish()

    datas = []

    for memo in memos:
        try:
            info: dict[Any, Any] = loads(memo.user_info)
            datas.append(
                f"{memo.id}: {memo.url}:\n  用户名: {info.get('username','未知')}\n  昵称: {info.get('nickname','未知')} 身份: {info.get('role','未知')}"
            )
        except Exception as e:
            datas.append(f"{memo.id}: {memo.url}:\n  信息加载失败: {e}")

    await UniMessage("\n".join(datas)).send()


@memos.assign("default")
async def default_handler(memo_id: Match[int], session: EventSession, sqlSession: async_scoped_session):
    setting = await sqlSession.scalar(select(Setting).where(Setting.user_id == session.id1))

    if setting is None:
        await UniMessage("请先绑定memos").finish()

    memo = await sqlSession.scalar(select(Memo).where(Memo.id == memo_id.result).where(Memo.user_id == session.id1))

    if memo is None:
        await UniMessage("找不到对应memo身份").finish()

    setting.default_memo = memo.id

    sqlSession.add(setting)
    await sqlSession.commit()
    await UniMessage("设置成功").send()


@memos.assign("unbind")
async def unbind_handler(memo_id: Match[int], session: EventSession, sqlSession: async_scoped_session):
    memo = await sqlSession.scalar(select(Memo).where(Memo.id == memo_id.result).where(Memo.user_id == session.id1))

    if memo is None:
        await UniMessage("找不到对应memo身份").finish()

    await sqlSession.delete(memo)
    await sqlSession.commit()
    await UniMessage("删除成功").send()


@memos.assign("create")
async def create_handler(
    msg: UniMsg,
    msg_id: MsgId,
    content: Match[str],
    session: EventSession,
    sqlSession: async_scoped_session,
    memoAndClient: MemoAndClientDependency,
):
    tip = ""
    try:
        msg.get_message_id()
    except Exception:
        tip = "\n(消息id获取失败)"

    memo, client = memoAndClient

    try:
        data = await client.createMemoWithModel(content.result)
    except Exception as e:
        await UniMessage(f"创建失败: {e}").finish()

    try:
        for image in msg[Image]:
            raw_bytes = await get_image_bytes(image)

            if raw_bytes is None:
                continue

            await client.createResource(
                filename=image.name,
                content=image.raw_bytes,
                size=str(len(raw_bytes)),
                memo=data.name,
            )
    except Exception as e:
        await UniMessage(f"资源上传失败: {e}").send()

    success_msg = await UniMessage(f"创建成功\n{client.buildMemoUrl(data.uid)}" + tip).send(at_sender=True)

    message_ids = [msg_id]

    if reply := success_msg.get_reply():
        message_ids.append(reply.id)

    try:
        sqlSession.add(
            MemoRecord(
                memo=memo.id,
                name=data.name,
                uid=data.uid,
                session_persist_id=await get_session_persist_id(session),
                message_id=msg_id,
                message_ids=message_ids,
                message=str(msg),
            )
        )
        await sqlSession.commit()
    except Exception as e:
        logger.exception(e)
        logger.error("memo记录创建失败")


@memos.assign("comment")
async def comment_handler(
    msg: UniMsg,
    msg_id: MsgId,
    ext: ReplyRecordExtension,
    uid: Match[str],
    content: Match[str],
    session: EventSession,
    sqlSession: async_scoped_session,
    memoAndClient: MemoAndClientDependency,
):
    memo, client = memoAndClient

    memo_name: str | None = None

    if uid.available:
        uid_result = uid.result

        if uid_result.isdigit():
            uid_result = f"memos/{uid_result}"

        if uid_result.startswith("memos/"):
            memo_name = uid_result
        else:
            if uid_result.isdigit():
                memo_name = f"memos/{uid_result}"
            else:
                try:
                    memoModel = await client.getMemoByUidWithModel(uid_result)
                    memo_name = memoModel.name
                except Exception as e:
                    await UniMessage(f"解析memo uid失败: {e}").finish()
    else:
        reply = ext.get_reply(msg_id)

        if reply is None:
            await UniMessage("未设置uid且没有回复相关消息").finish()

        memoRecord = await sqlSession.scalar(
            select(MemoRecord)
            .where(
                or_(
                    MemoRecord.message_id == reply.id,
                    MemoRecord.message_ids.contains(reply.id),
                )
            )
            .order_by(MemoRecord.created_at.desc())
            .limit(1)
        )

        if memoRecord is None:
            await UniMessage("未找到对应memo记录").finish()

        memo_name = memoRecord.name

    # if memo_name is None:
    #     await UniMessage("未找到对应memo记录").finish()

    try:
        data = await client.createCommentWithModel(memo_name, content.result)
    except Exception as e:
        await UniMessage(f"创建评论失败: {e}").finish()

    success_msg = await UniMessage(f"评论成功\n{client.buildMemoUrl(data.uid)}").send(at_sender=True)

    message_ids = [msg_id]

    if reply := success_msg.get_reply():
        message_ids.append(reply.id)

    sqlSession.add(
        MemoRecord(
            memo=memo.id,
            name=data.name,
            uid=data.uid,
            session_persist_id=await get_session_persist_id(session),
            message_id=msg_id,
            message_ids=message_ids,
            message=str(msg),
        )
    )
    await sqlSession.commit()


@memos.assign("link")
async def link_handler(
    msg: UniMsg,
    msg_id: MsgId,
    ext: ReplyRecordExtension,
    uid: Match[str],
    sqlSession: async_scoped_session,
    memoAndClient: MemoAndClientDependency,
):
    _, client = memoAndClient

    memo_uid: str | None = None

    memoRecord: MemoRecord | None = None

    if uid.available:
        uid_result = uid.result

        if uid_result.isdigit():
            uid_result = f"memos/{uid_result}"
        if uid_result.startswith("memos/"):
            try:
                memo = await client.getMemoByNameWithModel(uid_result)
                memo_uid = memo.uid
            except Exception as e:
                await UniMessage(f"解析memo uid失败: {e}").finish()

        else:
            memo_uid = uid_result

        memoRecord = await sqlSession.scalar(
            select(MemoRecord).where(MemoRecord.uid == memo_uid).order_by(MemoRecord.created_at.desc()).limit(1)
        )

        if memoRecord:
            memoRecord.message_ids.append(msg_id)
    else:
        reply = ext.get_reply(msg_id)

        if reply is None:
            await UniMessage("未设置uid且没有回复相关消息").finish()

        memoRecord = await sqlSession.scalar(
            select(MemoRecord)
            .where(
                or_(
                    MemoRecord.message_id == reply.id,
                    MemoRecord.message_ids.contains(reply.id),
                )
            )
            .order_by(MemoRecord.created_at.desc())
            .limit(1)
        )

        if memoRecord is None:
            await UniMessage("未找到对应memo记录").finish()

        memoRecord.message_ids.append(msg_id)

        memo_uid = memoRecord.uid

    receipt = await UniMessage(f"{client.buildMemoUrl(memo_uid)}").send(reply_to=msg.get_message_id())

    if memoRecord:
        if reply := receipt.get_reply():
            memoRecord.message_ids.append(reply.id)

        memoRecord.message_ids = memoRecord.message_ids[:]
        sqlSession.add(memoRecord)

    await sqlSession.commit()
