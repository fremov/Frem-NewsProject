import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import logging

# Настройка логов, чтобы видеть, что происходит
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    def __init__(self, base_url):
        self.base_url = base_url
        self.logger = logger
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def fetch_html(self, url):
        """Скачивает HTML код страницы"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status() # Выдаст ошибку, если сайт недоступен
            return response.text
        except requests.RequestException as e:
            logger.error(f"Ошибка при запросе к {url}: {e}")
            return None

    def get_soup(self, html):
        """Превращает текст в объект BeautifulSoup для удобного поиска"""
        if html:
            return BeautifulSoup(html, "lxml")
        return None

    @abstractmethod
    def parse(self):
        """
        Этот метод ДОЛЖЕН быть реализован в каждом конкретном парсере.
        Здесь будет логика поиска заголовков, картинок и т.д.
        """
        pass

    def run(self):
        """Запуск процесса"""
        logger.info(f"Начинаю парсинг: {self.base_url}")
        return self.parse()