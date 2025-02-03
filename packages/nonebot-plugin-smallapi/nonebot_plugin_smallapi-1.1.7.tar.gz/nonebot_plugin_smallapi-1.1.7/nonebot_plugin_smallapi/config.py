from nonebot.plugin import get_plugin_config
from pydantic import AnyHttpUrl, BaseModel, Field
from nonebot import logger

class Config(BaseModel):
    token: str = Field(alias="smallapi_token")

LOAD_OK = False

try:
    config: Config = get_plugin_config(Config)
except:
    logger.error(f"Smallapi V1.1.7 Plugin get config faild or the config is Null !")
    config = True

LOAD_OK = True