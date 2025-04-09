
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
- 🛠️ **灵活性**：基于文件的 config 设置，方便地对不同群、用户配置不同选项
- 🏗️ **易用性**：简单的 API 设计，方便上手  
- ☁️ **环境感知**：自带时间、天气等信息的动态注入，后续提供更多的环境信息注入  


## 📦 安装  

### 方式 1：通过 pip 安装
```sh
pip install nonebot-plugin-anywhere-llm
```



## 🚀 快速使用

### 配置
`.env`
```conf
OPENAI_API_KEY="sk-ivwnsnscugorsxqvncgbysxkcsnkccwagebmdqoluuwjlkmk"
OPENAI_BASE_URL="https://api.siliconflow.cn/v1"   # 代理地址
OPENAI_MODEL="deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"

LOCALSTORE_USE_CWD="true" # localstore 设置, 建议设置为 true
```

### 快速使用

```python

LLMService = require('nonebot_anywhere_llm').LLMService
llm = LLMService() # 默认配置


test_matcher = on_command("test")
@test_matcher.handle()
async def handle_ask(matcher: Matcher, event: MessageEvent):  
    output = await llm.generate('回复测试', event)
    await matcher.finish(output)

```

### 通过文件加载

```python
llm = LLMService.load('my_config.yaml') # 基于文件
llm.save('my_config.yaml') # 保存到 nonebot 插件的 config 目录, 跳过 api_key
```
文件中缺失的参数会使用默认值


### 动态参数设置

```python

LLMService = require('nonebot_anywhere_llm').LLMService
llm = LLMService()
print(llm.to_dict())
llm.config.params.temperature = 0.5
```

### system_prompt 模板设置与渲染说明
`config.system_prompt`下的所有选项接受字符串与文件，其中 `template` 将在 `<current_working_dir>/data/template`下查找，其他会在`<current_working_dir>/data/avatar`下查找  
假设通过 `.load(my_config)` 加载配置
```yaml
# my_config.yaml
...

system_prompt:
  template: template.md
  avatar: atri.md
  name: ...
  age: ...

```
构建`system_prompt`时会对 `template` 进行渲染   
`template.md`
```text
## 你的任务是根据[角色信息]扮演角色...

### 姓名 ${name}
### 年龄 ${age}
...

## 角色信息
${avatar}

...

```
`system_prompt` 下 `template` 外的其他选项渲染到`template`中, 程序会自动检查目录下对应名字的`.md` `.txt`


### 时间感知与~~天气感知~~
```python
# 设置config.md 或者代码中调整
llm.config.messages.injections.time= 1｜2｜3 # 默认 1
llm.config.messages.injections.weather= 1 # 没做 默认 0
```
需要在`config.system_prompt`设置对应的`${}`
```
...
## 当前时间 ${time}
## 天气 ${weather}
```


## TODO
- 更具体的时间信息 (工作日、假期、节假日)
- 天气、地点感知 
- 更适合群聊的config设计

## 📜 许可证  

本项目基于 [MIT License](LICENSE) 许可证发布。

💡 **喜欢这个项目？欢迎 Star⭐，让更多人看到！**




