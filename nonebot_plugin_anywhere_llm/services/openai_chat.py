from nonebot.log import logger
from sqlalchemy.ext.asyncio import AsyncSession

from .workspace_service import select_workspace
from .part_service import get_part
from openai import AsyncOpenAI




async def build_cfg_options(db: AsyncSession, workspace_sp: str) -> tuple[dict, dict]:
    """
    workspace_sp: workspace id or name
    return: (cfg_options, history_cfg)
    """
    workspace = await select_workspace(db, workspace_sp)
    if not workspace:
        raise ValueError(f"Workspace not found: {workspace_sp}")

    api_key = await get_part(db, workspace.active_model_parts["TOKEN"])
    model = await get_part(db, workspace.active_model_parts["MODEL_NAME"])
    base_url = await get_part(db, workspace.active_model_parts.get("URL"))
    
    cfg = {}
    cfg['temperature'] = workspace.engine_params.get('temperature', None)
    cfg['maxOutputTokens'] = workspace.engine_params.get('maxOutputTokens', None)
    cfg['top_p'] = workspace.engine_params.get('TopP', None)
    cfg['frequencyPenalty'] = workspace.engine_params.get('frequencyPenalty', None)
    cfg['presencePenalty'] = workspace.engine_params.get('presencePenalty', None)


    cfg['api_key'] = api_key.value
    cfg['model'] = model.value  
    cfg['base_url'] = base_url.value
    cfg['resolved_system_prompt'] = workspace.resolved_system_prompt

    logger.info(workspace.engine_params)
    history_cfg = {
        "timeWindowMinutes": workspace.history_strategy['timeWindowMinutes'],
        "maxCount": workspace.history_strategy['maxCount']
    }

    return cfg, history_cfg




async def call_openai(cfg: str, prompt: str, history: list = []) -> str:
    """
    cfg: model config dict
    prompt: user current prompt
    history: list of {"role": "user"/"assistant", "content": "..."}
    """


    client = AsyncOpenAI(
        api_key=cfg['api_key'],
        base_url=cfg['base_url']
    )
    response = await client.chat.completions.create(
        model=cfg['model'],
        messages=[ 
            {"role": "system", "content": cfg['resolved_system_prompt']},
            *history,
            {"role": "user", "content": prompt},

        ],
        temperature=cfg["temperature"],
        max_tokens=cfg["maxOutputTokens"],
        top_p=cfg["top_p"],
        frequency_penalty=cfg["frequencyPenalty"],
        presence_penalty=cfg["presencePenalty"],
    )
    
    return response.choices[0].message.content