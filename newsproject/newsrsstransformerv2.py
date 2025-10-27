import feedparser
from typing import List, Dict

# Нова функція для читання джерел з файлу
def load_sources(file_path: str) -> List[str]:
    """Зчитує список RSS-стрічок з текстового файлу, ігноруючи порожні рядки та коментарі."""
    sources = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Ігноруємо порожні рядки та рядки, що починаються з '#' (коментарі)
                if line and not line.startswith('#'):
                    sources.append(line)
    except FileNotFoundError:
        print(f"Помилка: Файл джерел '{file_path}' не знайдено.")
        return []
    
    print(f"Успішно завантажено {len(sources)} джерел з файлу.")
    return sources

def fetch_news(sources: List[str]) -> List[Dict]:
    """Збирає заголовки та посилання з усіх визначених RSS-стрічок."""
    all_news = []
    
    for url in sources:
        try:
            feed = feedparser.parse(url)
            
            for entry in feed.entries[:25]: # Обмежуємося останніми 25 новинами з кожного джерела
                all_news.append({
                    'title': entry.title,
                    'link': entry.link,
                    'published': entry.published if hasattr(entry, 'published') else 'N/A',
                    'source': url
                })
        
        except Exception as e:
            # Друк помилки для відстеження, яке джерело не спрацювало
            print(f"Помилка при обробці стрічки {url}: {e}")
            continue
            
    return all_news

# --- Запуск ---
if __name__ == "__main__":
    # Визначаємо шлях до нашого файлу
    SOURCES_FILE = "newsfeed.txt"
    
    # 1. Завантажуємо список джерел
    NEWS_SOURCES = load_sources(SOURCES_FILE)
    
    if NEWS_SOURCES:
        # 2. Збираємо новини
        collected_articles = fetch_news(NEWS_SOURCES)
        print(f"\nЗагалом зібрано {len(collected_articles)} новин.")

        # 3. Виведемо перші 5 новин
        print("\nПерші 5 зібраних новин:")
        for i, article in enumerate(collected_articles[:5]):
            print(f"--- Новина {i+1} ---")
            print(f"Заголовок: {article['title']}")
