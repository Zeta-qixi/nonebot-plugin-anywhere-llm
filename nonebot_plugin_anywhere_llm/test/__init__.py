from typing import Dict
from nonebot import require
from nonebot.matcher import Matcher
from nonebot import get_driver, on_command, on_message
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment



from .. import LLMParams, LLMService

my_params = LLMParams(
    model= "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",

)
llm = LLMService(my_params)

test_matcher = on_command("test")
@test_matcher.handle()
async def handle_ask(matcher: Matcher, event: GroupMessageEvent):  
    res = await llm.generate('回复测试')
    await matcher.finish(res)
    

