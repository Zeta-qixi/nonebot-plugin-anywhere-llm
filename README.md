
# ![Project Logo](https://github.com/Zeta-qixi/nonebot-plugin-anywhere-llm/blob/main/assets/logo.jpg)  
# nonebot-anywhere-llm  

> 为nonebot插件提供 LLM 接口

[![License](https://img.shields.io/github/license/Zeta-qixi/nonebot-plugin-anywhere-llm)](LICENSE)  
[![Stars](https://img.shields.io/github/stars/Zeta-qixi/nonebot-plugin-anywhere-llm)](https://github.com/Zeta-qixi/nonebot-plugin-anywhere-llm/stargazers)  
[![Issues](https://img.shields.io/github/issues/Zeta-qixi/nonebot-plugin-anywhere-llm)](https://github.com/Zeta-qixi/nonebot-plugin-anywhere-llm/issues)  

## ✨ 特性  

- 🚀 **快速**：开箱即用的LLM集成能力 
- 🛠️ **可扩展**：提供灵活的 config 与 prompt 设置
- 🏗️ **易用性**：简单的 API 设计，方便上手  

## 📦 安装  

### 方式 1：通过 pip 安装
```sh
pip install nonebot-plugin-anywhere-llm
```



## 🚀 快速使用
```python

LLMService = require('nonebot_anywhere_llm').LLMService
LLMParams = require('nonebot_anywhere_llm').LLMParams

my_params = LLMParams(
    model= "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
)

llm = LLMService(my_params)

test_matcher = on_command("test")
@test_matcher.handle()
async def handle_ask(matcher: Matcher, event: MessageEvent):  
    output = await llm.generate('回复测试')
    await matcher.finish(output)

```



## 📜 许可证  

本项目基于 [MIT License](LICENSE) 许可证发布。

💡 **喜欢这个项目？欢迎 Star⭐，让更多人看到！**




