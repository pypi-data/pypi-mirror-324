from pydantic import BaseModel

from nonebot.plugin import get_plugin_config


class Config(BaseModel):
    pass


config = get_plugin_config(Config)
