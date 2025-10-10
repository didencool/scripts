import feedparser
import requests
from typing import List, Dict

# Список RSS-стрічок, які ми будемо аналізувати
NEWS_SOURCES = [
    "https://www.reuters.com/arc/outboundfeeds/rss/?outputType=xml",
    "https://www.unian.ua/rss/news",
    "https://www.bbc.com/news/world/rss.xml",
]

def fetch_news(sources: List[str]) -> List[Dict]:
    """Збирає заголовки та посилання з усіх визначених RSS-стрічок."""
    all_news = []
    
    for url in sources:
        try:
            # Використовуємо feedparser, він дуже ефективний для RSS
            feed = feedparser.parse(url)
            
            # Обмежуємося останніми 20-30 новинами з кожного джерела
            for entry in feed.entries[:25]:
                # Додаємо новину у вигляді словника
                all_news.append({
                    'title': entry.title,
                    'link': entry.link,
                    'published': entry.published if hasattr(entry, 'published') else 'N/A',
                    'source': url
                })
        
        except Exception as e:
            print(f"Помилка при обробці стрічки {url}: {e}")
            continue
            
    print(f"Успішно зібрано {len(all_news)} новин.")
    return all_news

# --- Запуск ---
if __name__ == "__main__":
    collected_articles = fetch_news(NEWS_SOURCES)
    
    # Виведемо перші 5 новин, щоб перевірити, чи все працює
    print("\nПерші 5 зібраних новин:")
    for i, article in enumerate(collected_articles[:5]):
        print(f"--- Новина {i+1} ---")
        print(f"Заголовок: {article['title']}")
        print(f"Посилання: {article['link']}")
        print(f"Дата: {article['published']}")
