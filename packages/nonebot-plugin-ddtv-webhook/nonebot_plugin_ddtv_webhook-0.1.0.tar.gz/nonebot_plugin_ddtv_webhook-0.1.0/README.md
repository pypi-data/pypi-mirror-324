<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-ddtv-webhook

_✨ 处理DDTV WebHook并推送相关信息 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/Effect-Wei/nonebot-plugin-ddtv-webhook.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-ddtv-webhook">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-ddtv-webhook.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="python">

</div>

## 📖 介绍

有一个监控室大爷，他每天至少需要观看720小时来自$2^{64}$位不同管人的直播才能保证身心健康。因此，他的好朋友编写了本插件，以便第一时间通过 QQ Bot 告知大爷哪位管人开播或者下播了。

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-ddtv-webhook

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-ddtv-webhook
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-ddtv-webhook
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-ddtv-webhook
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot-plugin-ddtv-webhook"]

</details>

## ⚙️ 配置

Webhook URL查询字符串

| 配置项 | 必填  | 默认值 |                                  说明                                  |
| :----: | :---: | :----: | :--------------------------------------------------------------------: |
| token  |  否   |   无   | 令牌；当与设置的 `ddtv_webhook_token` 相同时才会推送消息，否则返回 403 |

---

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

|           配置项           | 必填  |    默认值     |                                            说明                                            |
| :------------------------: | :---: | :-----------: | :----------------------------------------------------------------------------------------: |
|     ddtv_webhook_token     |  否   |      无       |                   令牌，若不设置则不会进行验证，所有人都可以触发 Webhook                   |
|    ddtv_webhook_send_to    |  否   |      无       |                          信息订阅者的 QQ 号，格式为 ["123", "456"]                           |
| ddtv_webhook_send_to_group |  否   |      无       |                          信息订阅群的群号，格式为 ["123", "456"]                           |
|     ddtv_webhook_route     |  否   | /ddtv_webhook |                                       Webhook 的 URI                                       |
|         superusers         |  是   |      无       | Bot 管理员 QQ 号，在什么都没填的情况下默认将所有消息发给 Bot 管理员，格式为 ["123", "456"] |
