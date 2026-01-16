
<div align="center">

  <a href="https://nonebot.dev/">
    <img src="https://nonebot.dev/logo.png" width="200" height="200" alt="nonebot">
  </a>

# nonebot-plugin-anywhere-llm


_为你的 [nonebot2](https://github.com/nonebot/nonebot2) 插件提供 LLM 接口_

<p align="center">
  <img src="https://img.shields.io/github/license/Zeta-qixi/nonebot-plugin-anywhere-llm" alt="license">
  <img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/nonebot-2.4.0+-red.svg" alt="NoneBot">

</p>

</div>



## ✨ 特性  

- 🚀 **快速**：开箱即用的LLM集成能力 
- 🛠️ **灵活性**：拖拽式，方便地对不同群、用户配置不同选项
- 🏗️ **易用性**：简单的 API 设计，方便上手  
- ☁️ **环境感知**：自带时间、天气等信息的动态注入，后续提供更多的环境信息注入  


## 📦 安装  

### 方式 1：通过 pip 安装
```sh
pip install nonebot-plugin-anywhere-llm
```
需要开启fastapi




### 快速使用
加入插件后启动nonebot  
访问：`http://127.0.0.1:8080/llm-bridge` 配置

```python

from nonebot import on_command, require
from nonebot.adapters.onebot.v11 import MessageEvent
simple_chat = require('nonebot_plugin_anywhere_llm').simple_chat
matcher = on_command("ask")

@matcher.handle()
async def _(event: MessageEvent):
    reply = await simple_chat(
        workspace_name="CHAT", # 对应模板，大小写敏感
        prompt="你好"
    )
    
    await matcher.finish(reply)

```

## TODO
- 代码侧注入
- 天气、地点感知 
- 后处理（尤其是对带有think的模型）


## 📜 许可证  

本项目基于 [MIT License](LICENSE) 许可证发布。

💡 **喜欢这个项目？欢迎 Star⭐，让更多人看到！**




