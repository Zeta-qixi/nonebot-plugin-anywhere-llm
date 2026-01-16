from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from nonebot import get_driver, logger, get_app
from nonebot.plugin import PluginMetadata

from .config import plugin_config, Config
from .database import init_db, AsyncSessionLocal
from .services.history_manager import HistoryManager
from .services.openai_chat import build_cfg_options, call_openai
from .routes import module_api, part_api, workspace_api, openai_api

__plugin_meta__ = PluginMetadata(
    name="LLM Bridge",
    description="Based on SQLAlchemy Async",
    usage="...",
    config=Config,
)

# fastapi
app = get_app()
app.include_router(module_api.router, prefix="/llm-bridge/api")
app.include_router(part_api.router, prefix="/llm-bridge/api")
app.include_router(workspace_api.router, prefix="/llm-bridge/api")
app.include_router(openai_api.router, prefix="/llm-bridge/api")
PLUGIN_DIR = Path(__file__).parent
DIST_DIR = PLUGIN_DIR / "web" / "dist"
                            
if DIST_DIR.exists():
    logger.info(f"Mounting frontend static files from {DIST_DIR}")
    app.mount("/assets", StaticFiles(directory=DIST_DIR / "assets"), name="assets")
    @app.get("/llm-bridge")
    async def serve_spa():
        index_path = DIST_DIR / "index.html"
        return HTMLResponse(index_path.read_text(encoding='utf-8'))
else:
    logger.warning(f"Frontend dist folder not found at {DIST_DIR}")



# 自动建表
driver = get_driver()
@driver.on_startup
async def _():
    logger.info("Initializing LLM History Database...")
    await init_db()



# --- 对外核心接口 ---
from .services.bridge import chat_service

async def simple_chat(
    user_id: str, 
    group_id: str, 
    workspace_name: str, 
    prompt: str
) -> str:
    """
    [对外接口] 一键对话函数。
    自动管理数据库连接生命周期，调用者无需关心 DB。
    """
    # 1. 在函数内部创建 Session
    async with AsyncSessionLocal() as db:
        try:
            # 2. 调用核心业务逻辑 (复用 bridge.py)
            response = await chat_service(
                db=db, 
                user_id=user_id, 
                group_id=group_id, 
                workspace_name=workspace_name, 
                prompt=prompt
            )
            
            await db.commit()
            return response
            
        except Exception as e:
            await db.rollback()
            raise e
            