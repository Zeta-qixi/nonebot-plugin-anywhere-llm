from abc import ABC, abstractmethod
from string import Template
from typing import Dict
import re
class PromptTemplate(ABC):
    """模板基类"""
    @abstractmethod
    def render(self) -> Dict[str, str]:
        pass


class SystemPromptTemplate(PromptTemplate):
    """系统提示模板"""
    def __init__(self, template: str, role: str = "system"):
        self.template = Template(template)
        self.role = role
        self.context = {}

    def set_context(self, context: Dict) -> None:
        self.context = context

    def render(self) -> Dict[str, str]:

        content = self.template.substitute(self.context)
        return {"role": self.role, "content": content}
    

class UserPromptTemplate(PromptTemplate):
    """用户动态模板 主要是用户身份 用与群聊"""
    def __init__(self, role: str = "user"):
        self.role = role

    def set_role_list(self, context: Dict) -> None:
        ## TODO
        self.context = context
        ##默认 通过 config（master 默认称呼..） 或 动态 设置 user 的身份
        ## 先试试不修改system prompt 有没有效果

    def render(self, user_id: str = None) -> Dict[str, str]:
        
        if user_id:
            ...
        content = self.context.get("user_input", "")
        return {"role": self.role, "content": str(content)}
    

