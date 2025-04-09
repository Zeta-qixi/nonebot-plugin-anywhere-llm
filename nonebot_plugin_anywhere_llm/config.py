from pydantic import BaseModel, Field
from nonebot import get_plugin_config
from nonebot import require

from pydantic import BaseModel, Field, PositiveInt
from typing import Literal, Dict

require("nonebot_plugin_localstore")
import nonebot_plugin_localstore as store

DATA_DIR = store.get_plugin_data_dir()
Config_DIR = store.get_plugin_config_dir()
AVATAT_DIR = DATA_DIR / 'avatar'
TEMPLATE_DIR = DATA_DIR /'template'
DB_PATH = store.get_plugin_data_file("history.db")
for path in [AVATAT_DIR, TEMPLATE_DIR]:
    path.mkdir(parents=True, exist_ok=True)

class Config(BaseModel):

    openai_base_url: str = Field(default=None)
    openai_api_key: str = Field(default='')
    openai_model: str = Field(default='deepseek-ai/DeepSeek-R1-Distill-Qwen-7B')
    
llm_config = get_plugin_config(Config)



class LLMParams(BaseModel):
    """模型基础参数配置"""
    api_key: str = llm_config.openai_api_key
    base_url: str = llm_config.openai_base_url
    model: str = llm_config.openai_model
    temperature: float = 0.7
    max_tokens: int = 2000
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
        

class PromptInjectionConfig(BaseModel):
    """提示词注入配置"""
    time: Literal[0, 1, 2, 3] = 1
    weather: Literal[0, 1] = 0
    
    
class HistoryConfig(BaseModel):
    """ History 配置"""
    db_path: str = str(DB_PATH)
    max_length: PositiveInt = Field(10, gt=0, description="最大历史记录条数")
    time_window: PositiveInt = Field(86400, description="历史记录时间窗口（秒）")
    


class SystemPromptConfig(BaseModel):
    """系统提示配置"""
    template: str = Field(
        "你是一个由openai公司开发的大模型gpt",
        description="基础提示词模板"
    )
    class Config:
        extra = 'allow'
    

class MessagesConfig(BaseModel):
    
    history: HistoryConfig = Field(default_factory=HistoryConfig)
    system_prompt: SystemPromptConfig = Field(default_factory=SystemPromptConfig)
    injections: PromptInjectionConfig = Field(default_factory=PromptInjectionConfig)
    
    
class AppConfig(BaseModel):
    """聚合应用配置"""
    params: LLMParams = Field(default_factory=LLMParams)
    messages: MessagesConfig = Field(default_factory=MessagesConfig)
    
        


    
    
    