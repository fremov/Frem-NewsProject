from app.db.session import SessionLocal, engine
from app.db.models import Base, NewsItem
from scrapers.base import logger
from scrapers.sites.ign import SpecificSiteScraper
from scrapers.sites.habr import HabrScraper  # Импортируем новый класс

Base.metadata.create_all(bind=engine)


def run_sync_scraper():
    db = SessionLocal()

    # Список всех твоих парсеров
    scrapers = [
        SpecificSiteScraper("https://www.ign.com/pc?filter=popular"),
        HabrScraper("https://habr.com/ru/articles/")
    ]

    for scraper in scrapers:
        logger.info(f"--- Запуск парсера для: {scraper.base_url} ---")
        articles = scraper.parse(db_session=db)                                             
        if articles:
            for item in articles:
                new_entry = NewsItem(
                    title=item['title'],
                    content=item['content'],
                    source_url=item['source_url'],
                    source=item['source']
                )
                db.add(new_entry)

            db.commit()
            print(f"Добавлено новых новостей: {len(articles)}")

    db.close()


if __name__ == "__main__":
    run_sync_scraper()
