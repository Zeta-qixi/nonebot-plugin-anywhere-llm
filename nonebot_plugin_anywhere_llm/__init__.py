
from .llm_service import LLMService
from .provider import OpenAIProvider
from .models import LLMParams
from .utils import *
from .config import Config
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-anywhere-llm",
    description="为插件提供 LLM 访问能力， 统一记忆管理，支持多种模型参数和自定义 Prompt",
    type="library",
    usage='创建 llm_service 在插件内使用',
    homepage="https://github.com/Zeta-qixi/nonebot-plugin-anywhere-llm",
    config=Config,
    supported_adapters={"~onebot.v11"},
)


