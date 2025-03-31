from typing import Dict, List, Any
from pydantic import BaseModel, Field
from nonebot import get_plugin_config, get_driver
from nonebot import require
require("nonebot_plugin_localstore")
import nonebot_plugin_localstore as store

DATA_DIR = store.get_plugin_data_dir()
DB_PATH = store.get_plugin_data_file("history.db")


class Config(BaseModel):

    openai_base_url: str = Field(default=None)
    openai_api_key: str = Field(default='')
    openai_model: str = Field(default='deepseek-ai/DeepSeek-R1-Distill-Qwen-7B')
    
llm_config = get_plugin_config(Config)




class LLMParams:
    """模型基础参数配置"""
    def __init__(
        self,
        api_key: str = llm_config.openai_api_key,
        base_url: str = llm_config.openai_base_url,
        model: str = llm_config.openai_model,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,

    ):
        self.model = model
        self.api_key = api_key
        self.base_url = base_url
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"'{self.__class__.__name__}'对象没有属性'{key}'")