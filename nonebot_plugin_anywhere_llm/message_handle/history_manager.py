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
    
    @abstractmethod
    async def save_message(self, session_id: str, role: str, content: str) -> None:
        pass

    @abstractmethod
    async def get_history(
        self, 
        session_id: str
    ) -> List[Dict]:
        pass
    
    @abstractmethod
    async def clear_history(self, session_id: str) -> None:
        pass
    



class SQLiteHistoryManager(IHistoryManager):
    
    def __init__(self, db_path: str,):
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

        async with self.write_lock:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    "INSERT INTO history (session_id, role, content) VALUES (?, ?, ?)",
                    (session_id, role, content)
                )
                await db.commit()


    async def get_history(self, 
        session_id: str, length: int, seconds: int
    ) -> List[Dict[str, str]]:
        
        if not length:
            return []

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
    "SQLiteHistoryManager", 
]