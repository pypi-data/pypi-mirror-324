from typing import Union

from fastapi import FastAPI, status, HTTPException
from nonebot import get_plugin_config, get_bot, get_driver
from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment
from nonebot.drivers import Driver, ReverseMixin
from nonebot.plugin import PluginMetadata
from nonebot.log import logger

from .config import Config, DdtvWebhookBody


__plugin_meta__ = PluginMetadata(
    name="DDTV WebHook处理器",
    description="处理DDTV WebHook并推送相关信息",
    usage="配置订阅者QQ号并在DDTV中配置WebHook URL以接收DDTV信息",
    type="application",
    homepage="https://github.com/Effect-Wei/nonebot-plugin-ddtv-webhook",
)


driver: Driver = get_driver()
config = get_plugin_config(Config)

if not isinstance(driver, ReverseMixin) or not isinstance(driver.server_app, FastAPI):
    raise NotImplementedError("Only FastAPI reverse driver is supported.")


ID = Union[str, int]


app = FastAPI()


@app.post(config.ddtv_webhook_route, status_code=200)
async def push(
    r: DdtvWebhookBody,
    token: str | None = None,
):
    if config.ddtv_webhook_token is not None and token != config.ddtv_webhook_token:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    if r.cmd == "StartLiveEvent":
        msg = Message.template(
            MessageSegment.text("{name}正在直播：\n")
            + MessageSegment.text("{title}\n")
            + MessageSegment.text("https://live.bilibili.com/{RoomId}\n")
            + MessageSegment.image(r.data.cover_from_user.Value)
        ).format_map(
            {
                "name": r.data.Name,
                "title": r.data.Title.Value,
                "RoomId": r.data.RoomId,
            }
        )
    elif r.cmd == "StopLiveEvent":
        msg = Message.template(
            MessageSegment.text("{name}下播了\n")
            + MessageSegment.image(r.data.cover_from_user.Value)
        ).format_map({"name": r.data.Name})
    else:
        raise HTTPException(status.HTTP_200_OK)

    bot: Bot = get_bot()

    if config.ddtv_webhook_send_to is None:
        if config.ddtv_webhook_send_to_group is None:
            uids = config.superusers
        else:
            uids = []
    else:
        uids = config.ddtv_webhook_send_to

    for uid in uids:
        await bot.send_msg(user_id=uid, message=msg, message_type="private")

    if config.ddtv_webhook_send_to_group is None:
        gids = []
    else:
        gids = config.ddtv_webhook_send_to_group

    for gid in gids:
        await bot.send_msg(group_id=gid, message=msg, message_type="group")

    raise HTTPException(status.HTTP_200_OK)


@driver.on_startup
async def startup():
    if not config.ddtv_webhook_token:
        logger.warning("You are running without setting a token")

    driver.server_app.mount("/", app)
    logger.info(f"Mounted to {config.ddtv_webhook_route}")
