from abc import ABC, abstractmethod
import re
import os
from pathlib import Path
from string import Template
from typing import Dict, Union
from nonebot import logger

from ..config import SystemPromptConfig, AVATAT_DIR, TEMPLATE_DIR

class DefaultDict(dict):
    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:
            logger.warning(f"Key '{key}' is missing, replaced with empty string")
            return ''
        
        
        
class PromptTemplate(ABC):
    """Prompt模板基类"""
    _PATH_PATTERN = re.compile(r'^Path\((.*)\)$', re.IGNORECASE)
    

    def _resolve_value(self, value: Union[str, Path]) -> str:
        """统一解析值：处理文件路径或直接返回值"""
        if isinstance(value, (str, Path)):
            str_value = str(value).strip()
            match = self._PATH_PATTERN.match(str_value)
            if match:
                file_path = match.group(1).strip('\'"')
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        return f.read()
                except Exception as e:
                    raise ValueError(f"文件读取失败 [{file_path}]: {str(e)}")
            return str_value
        return value
    
    @abstractmethod
    def render(self) -> Dict[str, str]:
        pass
    
    @staticmethod
    def load_template(template: str, dir: Path) -> str:
        """加载模板内容，处理文件路径或直接返回模板字符串"""
        if len(template) <= 20:
            for ext in ['.md', '.txt', '']:
                for file in [dir/(template+ext), Path(template+ext)]:
                    try:
                        if file.is_file():
                            logger.info(f'加载模板成功: {file}')
                            return file.read_text( encoding="utf-8")
                    except Exception as e:
                        ...
        return template


class SystemPromptTemplate(PromptTemplate):
    """系统提示模板"""
    def __init__(self, config: SystemPromptConfig):
        
        self.context = DefaultDict()
        for k, v in config.model_dump().items():
            if k == 'template':
                self.template = Template(self.load_template(v, TEMPLATE_DIR))
            else:
                self.context[k] = self.load_template(v, AVATAT_DIR)
        
            
    def set_context(self, context: Dict) -> None:
        self.context.update(context)

    def render(self) -> Dict[str, str]:
        content = self.template.substitute(self.context)
        return {"role": 'system', "content": content}
    

class UserPromptTemplate(PromptTemplate):
    """用户动态模板 主要是用户身份 用与群聊"""
    def __init__(self, role: str = "user"):
        self.role = role

    def set_role_list(self, context: Dict) -> None:
        ## TODO
        self.context = context
        ## 默认 通过 config（master 默认称呼..） 或 动态 设置 user 的身份
        ## 先试试不修改system prompt 有没有效果

    def render(self, user_id: str = None) -> Dict[str, str]:
        
        if user_id:
            ...
        content = self.context.get("user_input", "")
        return {"role": self.role, "content": str(content)}
    

