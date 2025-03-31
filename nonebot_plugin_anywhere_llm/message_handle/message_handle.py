from typing import Dict, List, Callable

from .history_manager import SQLiteHistoryManager
from .prompt_templates import PromptTemplate, SystemPromptTemplate
from .injectors import InformationInjector, create_time_injector, create_weather_injector
from ..config import DB_PATH



class MessageHandler:
    def __init__(
        self,
        system_prompt: str = '你是一个猫娘',  
        set_time: int = 0, 
        set_weather: int = 0,
        db_path: str = DB_PATH,
        history_length: int = 10,
        time_window: int = 3600,
        auto_save: bool = True
    ):
        self.history_mgr = SQLiteHistoryManager(
            db_path=db_path,
            default_length=history_length,
            default_time=time_window,
            auto_save=auto_save
        )
        self.system_prompt = SystemPromptTemplate(system_prompt) 
        self.injector = InformationInjector()
        self.set_injector(set_time, set_weather)


    def set_injector(self, set_time: int, set_weather: int):
        """ set_time
        1: 基础time、
        2: 日期 季节
        3: 节日（工作日、假期）三天内的节日  （未实现）
        """
        self.injector.register_injector('time', create_time_injector(set_time))
        self.injector.register_injector('weather', create_weather_injector(set_weather))

    def add_injector(self, func: Callable[[str], str], priority):
        self.injector.register_injector(func, priority)
    
    async def save_message(self, session_id: str, role: str, content: str) -> None:
        await self.history_mgr.save_message(session_id, role, content)
        
        
    async def process_message(
        self,
        session_id: str,
        user_input: str|PromptTemplate,
        histroy_length: int | None = None,
        histroy_time: int | None = None,
        
    ) -> List[Dict[str, str]]:
        

        system_prompt = self.system_prompt.render()
        self.injector.inject(system_prompt)
        
   
        if isinstance(user_input, PromptTemplate):
            user_input = user_input.render()
        if isinstance(user_input, str): 
            user_input = {'role': 'user', 'content': user_input}
            
        histroy = await self.history_mgr.get_history(histroy_length, histroy_time)
        messages = [system_prompt] + histroy + [user_input]
        
        await self.save_message(session_id, user_input['role'], user_input['content'])
        
        return messages