from pathlib import Path
from ..config import DATA_DIR


def load_template( name: str, template_dir: str = DATA_DIR) -> str:
    """
    从模板目录加载模板文件，自动匹配 .md、.txt 或无扩展名文件
    
    """
    dir = Path(template_dir)
    for ext in ['.md', '.txt', '']:
        path = dir / f"{name}{ext}"
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                return f.read().strip()
    raise FileNotFoundError(f"未找到文件: {name}")