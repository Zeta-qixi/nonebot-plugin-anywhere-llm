from datetime import datetime, timedelta
import aiosqlite
import sqlite3
from typing import List, Dict
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import List, Dict
from asyncio import Lock



# 核心接口
class IHistoryManager(ABC):
    

    def __init__(
        self, 
        default_length: int = 10, 
        default_time: int = 3600 * 24,
        auto_save: bool = True  
    ):
        self.default_length = default_length
        self.default_time = default_time
        self.auto_save = auto_save 
        
        
    @abstractmethod
    async def save_message(self, session_id: str, role: str, content: str) -> None:
        pass

    @abstractmethod
    async def get_history(
        self, 
        session_id: str, 
        length: int | None = None, 
        seconds: int | None = None
    ) -> List[Dict]:
        pass
    
    @abstractmethod
    async def clear_history(self, session_id: str) -> None:
        pass
    



# 内存实现（带Token计数）
class MemoryHistoryManager(IHistoryManager):
    def __init__(
        self, 
        default_length: int = 10, 
        default_time: int = 3600 * 24,
        auto_save: bool = True,
        max_history_tokens: int = 2000
    ):
        super().__init__(default_length, default_time, auto_save)
        self.max_history_tokens = max_history_tokens
        self.histories = defaultdict(list)
        self.token_counts = defaultdict(int)


    async def save_message(self, session_id: str, role: str, content: str) -> None:
        if not self.auto_save:
            return
        new_tokens = self._count_tokens(content)
        current_time = datetime.now().isoformat()
        self.histories[session_id].append({
            "role": role,
            "content": content,
            "timestamp": current_time
        })
        self.token_counts[session_id] += new_tokens

        # 自动清理历史
        while self.token_counts[session_id] > self.max_history_tokens:
            if len(self.histories[session_id]) > 0:
                removed = self.histories[session_id].pop(0)
                self.token_counts[session_id] -= self._count_tokens(removed["content"])
            else:
                break


    async def get_history(self, 
        session_id: str, 
        length: int | None = None, 
        seconds: int | None = None
    ) -> List[Dict[str, str]]:
        
        length = length or self.default_length
        seconds = seconds or self.default_time
        
        result = []
        history = self.histories.get(session_id, [])
        cutoff = datetime.now() - timedelta(seconds=seconds)
        for message in reversed(history):
            if len(result) == length: break
            msg_time = datetime.fromisoformat(message["timestamp"])
            if msg_time >= cutoff:
                result.append({"role": message["role"], "content": message["content"]})
            else:
                break
            
        return result[::-1]

    async def clear_history(self, session_id: str) -> None:
        self.histories[session_id].clear()
        self.token_counts[session_id] = 0

    def _count_tokens(self, text: str) -> int:
        # 简易token计算（实际应使用tiktoken库）
        return len(text) // 4




class SQLiteHistoryManager(IHistoryManager):
    def __init__(self, 
        db_path: str = "data/llm/history.db",
        default_length: int = 10,
        default_time: int = 3600 * 24,
        auto_save: bool = True
    ):
        
        super().__init__(default_length, default_time, auto_save)
        self.write_lock = Lock()
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_path) as db:
            db.execute('''
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    role TEXT,
                    content TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            db.commit()


    async def save_message(self, session_id: str, role: str, content: str) -> None:
        ## TODO: add lock
        
        if not self.auto_save:
            return
        async with self.write_lock:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    "INSERT INTO history (session_id, role, content) VALUES (?, ?, ?)",
                    (session_id, role, content)
                )
                await db.commit()


    async def get_history(self, 
        session_id: str, 
        length: int | None = None, 
        seconds: int | None = None
    ) -> List[Dict[str, str]]:
        
        length = length or self.default_length
        seconds = seconds or self.default_time

        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT role, content FROM history WHERE "
                "session_id = ? AND timestamp >= datetime('now', ?)"
                "ORDER BY timestamp DESC LIMIT ?",
                (session_id,f'-{seconds} seconds',length,))
            rows = await cursor.fetchall()
        return [{"role": row[0], "content": row[1]} for row in reversed(rows)]
    
    
    
    async def clear_history(self, session_id: str) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM history WHERE session_id = ?", (session_id,))
            await db.commit()

__all__ = [
    "IHistoryManager",
    "MemoryHistoryManager",
    "SQLiteHistoryManager", 
]