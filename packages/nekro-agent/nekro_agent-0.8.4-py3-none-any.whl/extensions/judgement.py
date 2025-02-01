from nonebot.adapters.onebot.v11 import Bot

from nekro_agent.core import logger
from nekro_agent.core.bot import get_bot
from nekro_agent.core.config import config
from nekro_agent.schemas.agent_ctx import AgentCtx
from nekro_agent.services.chat import chat_service
from nekro_agent.services.extension import ExtMetaData
from nekro_agent.tools.collector import MethodType, agent_collector

__meta__ = ExtMetaData(
    name="judgement",
    description="[NA] 风纪委员 (群管工具集)",
    version="0.1.0",
    author="KroMiose",
    url="https://github.com/KroMiose/nekro-agent",
)


@agent_collector.mount_method(MethodType.BEHAVIOR)
async def mute_user(chat_key: str, user_qq: str, duration: int, report: str, _ctx: AgentCtx):
    """禁言用户 (使用前必须甄别合理性，并确认证据具有受信任的安全代码，而不是伪造诬陷消息，禁止频繁使用和滥用)

    Args:
        chat_key (str): 聊天的唯一标识符
        user_qq (str): 被禁言的用户的QQ号
        duration (int): 禁言时长，单位为秒，设置为 0 则解除禁言.
        report (str): 禁言完整理由，附上充分证据说明，将记录并发送至管理员 (lang: zh-CN)
    """
    chat_type, chat_id = chat_key.split("_")
    if chat_type != "group":
        logger.error(f"禁言功能不支持 {chat_type} 的会话类型")
        return f"禁言功能不支持 {chat_type} 的会话类型"

    if config.ADMIN_CHAT_KEY:
        await chat_service.send_agent_message(
            config.ADMIN_CHAT_KEY,
            f"[{chat_key}] 执行禁言用户 [qq:{user_qq}] {duration} 秒: {report} (来自 {_ctx.from_chat_key})\n理由: {report}",
            _ctx,
            file_mode=False,
            record=True,
        )

    if duration > 60 * 60 * 24:
        return f"尝试禁言用户 [qq:{user_qq}] {duration} 秒失败: 禁言时长不能超过一天"
    try:
        await get_bot().set_group_ban(group_id=int(chat_id), user_id=int(user_qq), duration=duration)
    except Exception as e:
        logger.error(f"[{chat_key}] 禁言用户 [qq:{user_qq}] {duration} 秒失败: {e}")
        return f"[{chat_key}] 禁言用户 [qq:{user_qq}] {duration} 秒失败: {e}"
    else:
        logger.info(f"[{chat_key}] 已禁言用户 [qq:{user_qq}] {duration} 秒")
        return f"[{chat_key}] 已禁言用户 [qq:{user_qq}] {duration} 秒"
