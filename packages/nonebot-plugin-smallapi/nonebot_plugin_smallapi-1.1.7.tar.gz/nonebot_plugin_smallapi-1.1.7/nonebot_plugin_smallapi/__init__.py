from .config import LOAD_OK, config
from nonebot.plugin import PluginMetadata

if LOAD_OK:
    try:
        from .api_menu import *
        from .api_pic import *
        from .api_text import *
        from .api_site import *
    except Exception as e:
        logger.error(f"Smallapi V1.1.7 Plugin load faild !")
        logger.exception(e)
    logger.success(f"Smallapi V1.1.7 Plugin is OK !")
    try:
        appkey = config.token
    except:
        appkey = "无"
    logger.info("读取您的故梦API密钥为：" + appkey)

__plugin_meta__ = PluginMetadata(
    name="小小API调用插件",
    description="调用api来操福Q民～",
    usage="发送“(API)图片/文字/站点系统”查看",
    type="application",
    homepage="https://github.com/chaichaisi/nonebot-plugin-smallapi",
    extra={
        "unique_name": "smallapi",
        "author": "Chaichaisi <chaichaisi@qq.com>",
        "version": "1.1.7",
    },
)
