
<div align="center">

  <a href="https://github.com/Zeta-qixi/nonebot-plugin-anywhere-llm/">
    <img src="https://github.com/Zeta-qixi/nonebot-plugin-anywhere-llm/blob/main/assets/logo.jpg" width="200">
  </a>

# nonebot-plugin-anywhere-llm


_✨ [Nonebot2](https://github.com/nonebot/nonebot2) 为nonebot插件提供 LLM 接口 ✨_

<p align="center">
  <img src="https://img.shields.io/github/license/Zeta-qixi/nonebot-plugin-anywhere-llm" alt="license">
  <img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/nonebot-2.4.0+-red.svg" alt="NoneBot">

</p>

</div>



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




