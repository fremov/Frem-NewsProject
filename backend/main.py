from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import SessionLocal
from app.db.models import NewsItem
from app.schemas.news import NewsSchema

app = FastAPI(title="News Aggregator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # В разработке разрешаем всем, в продакшене укажите адрес сайта
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Функция (Dependency), которая открывает базу перед запросом и закрывает после
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to News API! Go to /news to see articles."}

@app.get("/news", response_model=List[NewsSchema])
def get_news(db: Session = Depends(get_db)):
    """
    Возвращает список всех новостей из базы данных
    """
    # Запрашиваем новости из базы, сортируем по дате (свежие в начале)
    news = db.query(NewsItem).order_by(NewsItem.created_at.desc()).all()
    return news