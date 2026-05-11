from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles # Если понадобятся картинки/стили позже
from sqlalchemy.orm import Session
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import SessionLocal
from app.db.models import NewsItem
from app.schemas.news import NewsSchema

app = FastAPI(title="Frem News AI")

# Настройка шаблонов
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ГЛАВНАЯ СТРАНИЦА (HTML)
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, db: Session = Depends(get_db)):
    # Берем последние 30 новостей
    news = db.query(NewsItem).order_by(NewsItem.created_at.desc()).limit(30).all()
    return templates.TemplateResponse("index.html", {"request": request, "news": news})

# API для получения JSON (оставим для мобилки или тестов)
@app.get("/api/news", response_model=List[NewsSchema])
def get_news_json(db: Session = Depends(get_db)):
    return db.query(NewsItem).order_by(NewsItem.created_at.desc()).all()