import random

from nonebot import get_driver, require
from typing import Dict, List, Optional, Union
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent

from .message_handling import MessageHandler
from .provider import OpenAIProvider
from .config import LLMParams

# LLMService.py

class LLMService:
    def __init__(
        self, llm_param: LLMParams = None, 
        message_handle: MessageHandler = None
    ):
           
        self.param = llm_param or LLMParams()
        self.message_handle = message_handle or MessageHandler()
        
        self.provider = OpenAIProvider(self.param)
        


    async def generate(
            self,
            input: str,
            event: MessageEvent = None,
            save: bool = False,
            use_histroy: int = 0,
            histroy_time: int = 0, 
            **param
        ) -> str:
            
            self.param.update(**param)
            session_id = event.get_session_id() if event else 'default'
            messages = await self.message_handle.process_message(session_id, input, use_histroy, histroy_time)
            response = await self.provider.generate(
                messages = messages,
                params = self.param
            )
            if save:
                await self.message_handle.save_message(session_id, 'assistant' , response)
            return response



    async def chat(
            self,
            input: str,
            event: MessageEvent,
            use_histroy: int = 10,
            histroy_time: int = 3600, 
            **param
        ) -> str:
        
            self.param.update(param)
            session_id = event.get_session_id()
            messages = await self.message_handle.process_message(session_id, input, use_histroy, histroy_time)
            response = await self.provider.generate(
                messages = messages,
                params = self.param
            )
            await self.message_handle.save_message(session_id, 'assistant' , response)
            return response


    async def group_chat(
        self,
        prompt: str,
        event: GroupMessageEvent,
        use_histroy: int = 30,
        histroy_time: int = 300, 
        probability : float = 0.5, # 回复概率
        **param

    ) -> str:
        
        self.param.update(param)
        session_id = event.group_id()
        messages = await self.message_handle.process_message(session_id, input, use_histroy, histroy_time)
        response = await self.provider.generate(
            messages = messages,
            params = self.param
        )
        await self.message_handle.save_message(session_id, 'assistant' , response)
        return response