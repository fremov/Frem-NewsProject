from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Базовый класс, от которого будут наследоваться все наши таблицы
Base = declarative_base()

class NewsItem(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    source_url = Column(String, unique=True)
    source = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<NewsItem(title={self.title[:30]}...)>"