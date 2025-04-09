import yaml
import random
from pathlib import Path
from typing import Dict, Any
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent

from .message_handle import MessageHandler, PromptTemplate
from .config import AppConfig, Config_DIR
from .provider import openai_provider



def _flatten_dict(data: Dict, parent_key: str = '') -> list:
    """字典扁平化处理"""
    items = []
    for k, v in data.items():
        new_key = f"{parent_key}.{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(_flatten_dict(v, new_key))
        else:
            items.append((new_key, v))
    return items


# LLMService.py
class LLMService:
    def __init__(self,config: AppConfig = None):
        self._config = config or AppConfig()     

    @classmethod
    def load(cls, file_name: str | Path) -> 'LLMService':
        file_path = Config_DIR / file_name
        with open(file_path) as f:
            data = yaml.safe_load(f)
        return cls(AppConfig().model_copy(update=data))

    def __getattr__(self, name: str) -> 'LLMService':
            """实现链式调用"""
            if hasattr(self._config, name):
                self._current_path = getattr(self._config, name)
                return self
            raise AttributeError(f"无效配置项: {name}")
        
    def to_dict(self) -> Dict:
        """导出为字典"""
        return self._config.model_dump()

    def save(self, file_name: str | Path) -> None:
        data = self.to_dict()
        del(data['params']['api_key'])
        file_path = Config_DIR / file_name
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(
                data,
                f,
                allow_unicode=True,
                sort_keys=False
            )

    @property
    def config(self) -> AppConfig:
        return self._config
        
        
    async def generate(
            self,
            input: str,
            event: MessageEvent = None,
            save: bool = False,
        ) -> str:
            
            message_handle = MessageHandler(self.config.messages)
            session_id = event.get_session_id() if event else 'default'
            messages = await message_handle.process_message(session_id, input)
            response = await openai_provider.generate(
                messages = messages,
                params = self.config.params
            )
            if save:
                await message_handle.save_message(session_id, messages[-1])
                await message_handle.save_message(session_id, {'role': 'assistant' ,'content': response})
            return response
