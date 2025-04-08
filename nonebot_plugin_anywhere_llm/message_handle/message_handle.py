from typing import Dict, List, Callable

from .history_manager import SQLiteHistoryManager
from .prompt_templates import PromptTemplate, SystemPromptTemplate
from .injectors import InformationInjector, create_time_injector, create_weather_injector
from ..config import MessagesConfig


class MessageHandler:
    def __init__(self, config: MessagesConfig):
        
        self.history_mgr = SQLiteHistoryManager(
            db_path=config.history.db_path       
        )
        self.system_prompt = SystemPromptTemplate(
            config.system_prompt
        )
        self.injector = InformationInjector()
        self._setup_injectors(config.system_prompt)
        
        self.histroy_length=config.history.max_history_length
        self.histroy_time=config.history.time_window_seconds



    def set_injector(self, time_injection_level: int, weather_injection: int):
        """配置信息注入器
        
        Args:
            time_level: 时间信息等级
                0: 不注入
                1: 基础时间
                2: 日期+季节
                3: 节日信息（待实现）
            weather_level: 天气信息等级
                0: 不注入
                1: 基础天气
        """
        self.injector.register_injector(
            'time', 
            create_time_injector(time_injection_level))
        self.injector.register_injector(
            'weather', 
            create_weather_injector(weather_injection))


    def add_injector(self, func: Callable[[str], str], priority):
        self.injector.register_injector(func, priority)
    
    async def save_message(self, session_id: str, data: Dict[str, str]) -> None:
        await self.history_mgr.save_message(session_id, data.get('role'),  data.get('content'))
        
        
    async def process_message(
        self,
        user_input: str,
    ) -> List[Dict[str, str]]:
        

        system_prompt = self.system_prompt.render()
        self.injector.inject(system_prompt) 
        histroy = await self.history_mgr.get_history(self.histroy_length, self.histroy_time)
        user_input = {'role': 'user', 'content': user_input}
        messages = [system_prompt] + histroy + [user_input]
        
        return messages