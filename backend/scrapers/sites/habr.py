import time
from scrapers.base import BaseScraper, logger
from app.ai_utils import process_news_text

class HabrScraper(BaseScraper):
    def parse_article_details(self, url):
        """Заходит внутрь статьи Хабра и забирает весь текст с правильными отступами"""
        html = self.fetch_html(url)
        soup = self.get_soup(html)
        if not soup:
            return ""

        # Основной контейнер текста на Хабре
        content_node = soup.find("div", class_="article-formatted-body")
        if not content_node:
            return ""

        # На Хабре лучше искать только параграфы <p>.
        # Если статья старая, контент может быть просто разбит тегами <br>,
        # но современные статьи упакованы в <p>.
        paragraphs = content_node.find_all("p")

        # Если параграфов почему-то нет, пробуем взять прямой текст из дива
        if not paragraphs:
            # strip=True убирает лишние пробелы по краям
            return content_node.get_text(separator="\n\n", strip=True)

        # Собираем текст, разделяя абзацы двумя переносами
        clean_text = "\n\n".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])

        return clean_text

    def parse(self, db_session=None):
        html = self.fetch_html(self.base_url)
        soup = self.get_soup(html)
        if not soup:
            return []

        articles = []
        items = soup.find_all("article", class_="tm-articles-list__item")

        for item in items:
            title_node = item.find("a", class_="tm-title__link")

            if title_node:
                title = title_node.get_text(strip=True)
                relative_url = title_node.get("href", "")
                source_url = "https://habr.com" + relative_url

                if db_session:
                    from app.db.models import NewsItem
                    existing = db_session.query(NewsItem).filter(NewsItem.source_url == source_url).first()
                    if existing:
                        logger.info(f">>> Habr: '{title[:30]}...' уже в базе. Пропускаем.")
                        break

                logger.info(f"Habr: Попытка спарсить контент: {title[:40]}...")

                # Получаем контент
                full_content = self.parse_article_details(source_url)

                # --- КРИТИЧЕСКАЯ ПРОВЕРКА ---
                # Если контент пустой, меньше 100 символов или возникла ошибка таймаута
                if not full_content or len(full_content.strip()) < 100:
                    logger.warning(
                        f"!!! Habr: Контент статьи '{title[:30]}' пуст или слишком мал. Пропускаем запись в БД.")
                    continue  # Переходим к следующей новости в цикле, не добавляя в articles

                if full_content and len(full_content) > 100:
                    full_content = process_news_text(full_content)
                    articles.append({
                        "title": title,  # Оставляем как есть
                        "content": full_content,
                        "source_url": source_url,
                        "source": "Habr"
                    })

                time.sleep(1.5)

        return articles
