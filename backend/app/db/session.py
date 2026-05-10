from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Указываем путь к файлу базы данных внутри папки backend
SQLALCHEMY_DATABASE_URL = "sqlite:///./news.db"

# Создаем "движок" базы
# check_same_thread=False нужен только для SQLite, чтобы FastAPI мог работать с базой в разных потоках
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Создаем фабрику сессий (через сессии мы будем делать запросы)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)