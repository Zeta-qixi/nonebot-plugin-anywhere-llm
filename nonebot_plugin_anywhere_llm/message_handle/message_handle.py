from typing import Dict, List, Callable
from .history_manager import SQLiteHistoryManager
from .prompt_templates import  SystemPromptTemplate
from .injectors import InformationInjector, create_time_injector, create_weather_injector
from ..config import MessagesConfig, PromptInjectionConfig


class MessageHandler:
    def __init__(self, config: MessagesConfig):
        
        self.history_mgr = SQLiteHistoryManager(
            db_path=config.history.db_path)
        self.system_prompt = SystemPromptTemplate(
            config.system_prompt)
        self.injector = InformationInjector()
        self._setup_injectors(config.injections)
        
        self.histroy_length=config.history.max_length
        self.histroy_time=config.history.time_window


    def _setup_injectors(self, config: PromptInjectionConfig):
        """配置信息注入器
        
        Args:
            time_level: 时间信息等级
                0: 不注入
                1: 基础时间 2: 日期+季节 3: 节日信息（待实现）
            weather_level: 天气信息等级
                0: 不注入
                1: 基础天气
        """
        if config.time:
            self.injector.register_injector(
                'time', 
                create_time_injector(config.time))
        if config.weather:
            self.injector.register_injector(
                'weather', 
                create_weather_injector(config.weather))


    def add_injector(self, func: Callable[[str], str], priority):
        self.injector.register_injector(func, priority)
    
    async def save_message(self, session_id: str, data: Dict[str, str]) -> None:
        await self.history_mgr.save_message(session_id, data.get('role'),  data.get('content'))
        
        
    async def process_message(
        self,
        session_id: str,
        user_input: str,
    ) -> List[Dict[str, str]]:
        
        self.injector.inject(self.system_prompt) 
        system_prompt = self.system_prompt.render()
        histroy = await self.history_mgr.get_history(session_id, self.histroy_length, self.histroy_time)
        user_input = {'role': 'user', 'content': user_input}
        messages = [system_prompt] + histroy + [user_input]
        
        return messages