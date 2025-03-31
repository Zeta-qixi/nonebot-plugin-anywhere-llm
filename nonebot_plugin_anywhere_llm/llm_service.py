import random
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent

from .message_handle import MessageHandler, PromptTemplate
from .provider import OpenAIProvider
from .config import LLMParams


def get_provider_class(**kwargs):
    # TODO
    ...

# LLMService.py
class LLMService:
    def __init__(
        self, 
        message_handle: MessageHandler = None,
        llm_param: LLMParams = None, 
    ):
           
        self.param = llm_param or LLMParams()
        self.message_handle = message_handle or MessageHandler()
        self.provider = OpenAIProvider(self.param)
        
    @classmethod
    def from_config(cls, config: dict):
        # TODO
        """通过配置字典快速初始化"""
        llm_config = config.get('llm_params', {})
        msg_config = config.get('message_handle', {})
        
        return cls(
            llm_param=LLMParams(**llm_config),
            message_handle=MessageHandler.from_config(msg_config),
            provider_class=get_provider_class(llm_config.get('provider'))
        )


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
            user_input: str,
            event: MessageEvent,
            use_histroy: int = 10,
            histroy_time: int = 3600, 
            **param
        ) -> str:
        
            self.param.update(**param)
            session_id = event.get_session_id()
            messages = await self.message_handle.process_message(session_id, user_input, use_histroy, histroy_time)
            response = await self.provider.generate(
                messages = messages,
                params = self.param
            )
            await self.message_handle.save_message(session_id, 'assistant' , response)
            return response


    async def group_chat(
        self,
        user_input: str|PromptTemplate,
        event: GroupMessageEvent,
        use_histroy: int = 30,
        histroy_time: int = 300, 
        probability : float = 0.5, # 回复概率
        **param

    ) -> str:
        self.param.update(**param)
        session_id = event.group_id
        messages = await self.message_handle.process_message(session_id, user_input, use_histroy, histroy_time)
        
        if probability>=random.random():
            response = await self.provider.generate(
                messages = messages,
                params = self.param
            )
            await self.message_handle.save_message(session_id, 'assistant' , response)
            return response