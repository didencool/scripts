import feedparser
from typing import List, Dict

def load_sources(file_path: str) -> List[str]:
    """Завантажує URL-адреси RSS-стрічок із зазначеного файлу."""
    try:
        # Зверніть увагу, що file_path має бути повним шляхом до Google Drive
        with open(file_path, 'r', encoding='utf-8') as f:
            sources = [line.strip() for line in f if line.strip()]
        return sources
    except FileNotFoundError:
        print(f"Помилка: Файл джерел не знайдено за шляхом: {file_path}")
        return []

def fetch_news(rss_sources: List[str], limit_per_source: int) -> List[Dict]:
    """Збирає заголовки новин з усіх RSS-стрічок, обмежуючи кількість новин."""
    collected_articles = []

    for url in rss_sources:
        try:
            feed = feedparser.parse(url)
            print(f"Збір новин з: {url[:60]}...")

            for entry in feed.entries[:limit_per_source]:
                article = {
                    'title': entry.get('title', 'N/A'),
                    'link': entry.get('link', 'N/A'),
                    'source': url,
                }
                collected_articles.append(article)

        except Exception as e:
            print(f"Помилка при зборі новин з {url}: {e}")

    print(f"Зібрано {len(collected_articles)} статей загалом.")
    return collected_articles
