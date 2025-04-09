import datetime
from typing import Any, Callable, Dict, Tuple
from datetime import datetime
from collections import OrderedDict
from ..prompt_templates import SystemPromptTemplate



class InformationInjector:
    def __init__(self):

        self.injectors: Dict[str, Tuple[int, Callable[[Any], str]]] = OrderedDict()
    
    def register_injector(self, name: str, 
                         injector: Callable[[Any], str],
                         priority: int = 0,) -> None:
        
        self.injectors[name] = (priority, injector)
        
    def inject(self, system_prompt: SystemPromptTemplate) -> None:
        for name, (_, injector) in sorted(self.injectors.items(), key=lambda x: x[1][0]):
            system_prompt.set_context({name: injector()})
            


# ================================ #        
#           内置注入               
# ================================ #     
   
   
SEASON = [0, '冬', '冬', '春', '春', '春', '夏', '夏', '夏', '秋', '秋', '秋', '冬']
def llm_system_time() -> str:
    now = datetime.now()
    formatted_date = now.strftime("%D %H:%M %A ") + SEASON[now.month]
    return f"[{formatted_date}]" 


def create_time_injector(option: int) -> Callable[[str], str]:
    def time_injector() -> str:
        
        now = datetime.now()
        if option == 1:
            context = now.strftime("%H:%M")
        elif option == 2:
            context = now.strftime("%D %H:%M %A ") + SEASON[now.month]
        elif option == 3:
            # TODO add holiday
            context = now.strftime("%D %H:%M %A ") + SEASON[now.month]
        return context   
    return time_injector

def get_weather():
    ...
    

def create_weather_injector(option: int) -> Callable[[str], str]:
    def weather_injector() -> str:
        return get_weather()
    
    return weather_injector

__all__=["create_time_injector", "create_weather_injector"]