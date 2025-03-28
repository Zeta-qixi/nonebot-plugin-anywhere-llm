## 上下文管理器

- 模板 Prompt (如何设计，你想设计功能，怎么样的使用形式)
    - 默认模板
    - 自定义模板

- 额外信息注入器
    - 默认注入信息 时间、天气
    - 注册到管理器后之后自动调用 [情绪...]
    - 修改注入 （猫 --> 哈吉米）
     
- token计数器 (要实现不同插件使用的计算统计，能不能通过message对象定位到插件，那可以移到core中)
- 

## 参数管理器
- api 参数
- 超参数

## 调用步骤
1. 初始化 history_manager  | 可选
2. 实例 sys prompt
1. 初始化 message_handle（history_manager， system_prompt_template）
    1. 设置内置 infector       | 可选


1. message_handle 注册其他 infector  | 可选
2. 设置 history_manager 自动保存 、上下文使用数量

1. 注册 UserPromptTemplate



```python
sys = SystemPromptTemplate()
messagehandle = MessageHandle(
    # 上下文管理器 可用默认
    # system_prompt_template 传入 可以默认
)
user_prompt = UserPromptTemplate(...)

xxx = LLMParams(...)
# 参数管理器 & messagehandle-> 实例化 llm

# Prompt 和message 管理是传参 ，修改可以实现
llm.chat(
    input,
    session_id, # session_id是基于聊天，上下文管理器需要 session_id 
    user_id, ... # group_chat
    # 动态参数管理器 ？ 
)
```

## 还有需要考虑的
- 在哪里确定使用上下文范围 （肯定是希望直接用的）
- 现在是如何让插件联动的
- 模板用 __call__ 渲染？
- 模板也单作一种注入？

## 新功能准备
- 默认时间天气注入可以使用传入模板 %H%D ...

## 
```
class A:
    def __call__(self, x, y):
        return x + y
```