from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NewsSchema(BaseModel):
    id: int
    title: str
    content: Optional[str] = None
    source_url: str
    source: Optional[str] = None # ДОБАВЛЯЕМ ЭТО ПОЛЕ
    created_at: datetime

    class Config:
        from_attributes = True