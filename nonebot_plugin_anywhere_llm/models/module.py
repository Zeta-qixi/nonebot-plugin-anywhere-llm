from sqlalchemy import Column, String, Text, DateTime, JSON, func
from ..database import Base

class Module(Base):
    __tablename__ = "modules"
    id = Column(String(64), primary_key=True)
    name = Column(String(100), nullable=False)
    type = Column(String(32), nullable=False)
    content = Column(Text, nullable=True) # 假设 content 是字符串，如果是JSON请改用 JSON 类型
    created_at = Column(DateTime, server_default=func.now())