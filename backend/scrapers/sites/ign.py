import sys
import os
import time
from scrapers.base import BaseScraper, logger
from app.utils import translate_to_russian
import time
from app.ai_utils import process_news_text

# Пути для импорта BaseScraper
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

class SpecificSiteScraper(BaseScraper):
    def parse_article_details(self, url):
        html = self.fetch_html(url)
        soup = self.get_soup(html)
        if not soup: return ""

        content_section = soup.find("section", class_="article-page")
        if not content_section: return ""

        paragraphs = content_section.find_all("p")

        # ИЗМЕНЕНИЕ ЗДЕСЬ: меняем " " на "\n\n"
        text = "\n\n".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])

        return text

    def parse(self, db_session=None):
        html = self.fetch_html(self.base_url)
        soup = self.get_soup(html)
        if not soup: return []

        articles = []
        nodes = soup.find_all("div", class_="content-item")

        for node in nodes:
            link_tag = node.find("a", class_="item-body")
            title_tag = node.find("span", class_="item-title")

            if link_tag and title_tag:
                source_url = "https://www.ign.com" + link_tag.get("href", "")
                title_en = title_tag.get_text(strip=True)

                if db_session:
                    from app.db.models import NewsItem
                    if db_session.query(NewsItem).filter(NewsItem.source_url == source_url).first():
                        break

                logger.info(f"IGN: Перевод и парсинг: {title_en[:30]}...")

                content_en = self.parse_article_details(source_url)

                # ПЕРЕВОД
                title_ru = translate_to_russian(title_en)
                content_ru = translate_to_russian(content_en)

                if content_ru:
                    content_ru = process_news_text(content_ru)
                    articles.append({
                        "title": title_ru,
                        "content": content_ru,
                        "source_url": source_url,
                        "source": "IGN"
                    })
                time.sleep(1)
        return articles


if __name__ == "__main__":
    TEST_SITE_URL = "https://www.ign.com/pc?filter=popular"
    scraper = SpecificSiteScraper(TEST_SITE_URL)
    results = scraper.run()

    import pprint

    pprint.pprint(results)