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

    # model parts
    api_key = await get_part(db, workspace.active_model_parts["TOKEN"])
    model = await get_part(db, workspace.active_model_parts["MODEL_NAME"])
    base_url = await get_part(db, workspace.active_model_parts.get("URL"))
    
    cfg = workspace.engine_params.copy()
    cfg['api_key'] = api_key.value
    cfg['model'] = model.value  
    cfg['base_url'] = base_url.value
    cfg['resolved_system_prompt'] = workspace.resolved_system_prompt

    
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
        # temperature=cfg['engine_params']["temperature"],
        # max_tokens=cfg['engine_params']["maxOutputTokens"],
        # top_p=cfg['engine_params']["topP"],
        # frequency_penalty=cfg['engine_params']["frequencyPenalty"],
        # presence_penalty=cfg['engine_params']["presencePenalty"],
    )
    
    return response.choices[0].message.content