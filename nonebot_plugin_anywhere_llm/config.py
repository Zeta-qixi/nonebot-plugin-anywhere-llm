from pydantic import BaseModel, Field
from nonebot import get_plugin_config, get_driver


class Config(BaseModel):

    openai_base_url: str = Field(default=None)
    openai_api_key: str = Field(default='')
    openai_model: str = Field(default='deepseek-ai/DeepSeek-R1-Distill-Qwen-7B')
    
llm_config = get_plugin_config(Config)

