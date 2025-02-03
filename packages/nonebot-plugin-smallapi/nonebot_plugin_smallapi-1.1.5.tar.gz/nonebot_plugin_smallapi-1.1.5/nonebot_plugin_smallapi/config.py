from nonebot.plugin import get_plugin_config
from pydantic import AnyHttpUrl, BaseModel, Field
from nonebot import logger

class Config(BaseModel):
    token: str = Field(alias="smallapi_token")

LOAD_OK = False

try:
    config: Config = get_plugin_config(Config)
except Exception as e:
    logger.error(f"Smallapi V1.2.0 Plugin get config faild !")
    logger.exception(e)

LOAD_OK = True