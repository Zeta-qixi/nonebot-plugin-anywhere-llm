from collections import OrderedDict
import datetime
from typing import Callable, Dict
from .injector import InformationInjector
from datetime import datetime


SEASON = [0, '冬', '冬', '春', '春', '春', '夏', '夏', '夏', '秋', '秋', '秋', '冬']

def llm_system_time() -> str:
    now = datetime.now()
    formatted_date = now.strftime("%D %H:%M %A ") + SEASON[now.month]
    return f"[{formatted_date}]" 


def create_time_injector(option: int) -> Callable[[str], str]:
    def time_injector(context: str) -> str:
        assert option != 0, '跳过时间注入'
       
        now = datetime.now()
        if option == 1:
            msg = now.strftime("%H:%M")
        elif option == 2:
            msg = now.strftime("%D %H:%M %A ") + SEASON[now.month]
        elif option == 3:
            # TODO
            msg = now.strftime("%D %H:%M %A ") + SEASON[now.month]
        context += f"\n\n## 时间: {msg}"
        return context   
    return time_injector

def get_weather():
    ...
    

def create_weather_injector(option: int) -> Callable[[str], str]:
    def weather_injector(context: str) -> str:
        assert option != 0, '跳过天气注入'
        msg = get_weather()
        context += f"\n\n## 天气: {msg}"
        return context
    
    return weather_injector

__all__=["create_time_injector", "create_weather_injector"]