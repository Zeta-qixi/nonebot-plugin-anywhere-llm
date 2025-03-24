from typing import Dict, List, Any
from ..config import llm_config

class LLMParams:
    """模型基础参数配置"""
    def __init__(
        self,
        model: str = llm_config.openai_model,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        system_prompt: str = None
    ):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.system_prompt = system_prompt
        
    def get_system_prompt(self) -> List[Any]:
        if self.system_prompt:
            return [{"role": "system", "content": self.system_prompt}]