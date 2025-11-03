import feedparser
from typing import List, Dict

# ==========================================================
# ГЛОБАЛЬНІ ПАРАМЕТРИ
# ==========================================================
SOURCES_FILE = "newsfeed.txt"
NEWS_LIMIT = 75
# ==========================================================
# ... ініціалізація моделей ...


# Функція для завантаження джерел залишається без змін
def load_sources(file_path: str) -> List[str]:
    """Зчитує список RSS-стрічок з текстового файлу."""
    sources = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    sources.append(line)
    except FileNotFoundError:
        print(f"Помилка: Файл джерел '{file_path}' не знайдено.")
        return []

    return sources

def fetch_news(sources: List[str]) -> List[Dict]:
    """Збирає заголовки та посилання з усіх визначених RSS-стрічок, з розширеною обробкою."""
    all_news = []

    print(f"Розпочато збір новин з {len(sources)} джерел...")

    for url in sources:
        try:
            feed = feedparser.parse(url)
            count_fetched = 0

            # Перевірка, чи feedparser успішно обробив стрічку
            if not feed.entries:
                print(f"  [Попередження] Джерело {url}: не знайдено жодної 'entry'. Можливо, помилка парсингу.")
                continue

            for entry in feed.entries[:25]: # Обмежуємося останніми 25 новинами

                # Забезпечення наявності основних полів (title та link)
                title = getattr(entry, 'title', None)
                link = getattr(entry, 'link', None)
                published = getattr(entry, 'published', 'N/A')

                if title and link:
                    all_news.append({
                        'title': title,
                        'link': link,
                        'published': published,
                        'source': url
                    })
                    count_fetched += 1

            print(f"  [Успіх] З джерела {url} зібрано {count_fetched} новин.")

        except Exception as e:
            # Це відобразить будь-які інші непередбачені помилки
            print(f"  [Критична Помилка] Непередбачена помилка при обробці {url}: {e}")
            continue

    return all_news

# --- Запуск ---
if __name__ == "__main__":
    NEWS_SOURCES = load_sources(SOURCES_FILE)

    if NEWS_SOURCES:
        collected_articles = fetch_news(NEWS_SOURCES)
        print(f"\nЗагалом зібрано {len(collected_articles)} новин.")

        print("\nПерші 5 зібраних новин:")
        for i, article in enumerate(collected_articles[:NEWS_LIMIT]):
            print(f"--- Новина {i+1} ---")
            print(f"Джерело: {article['source'][:40]}...") # Обмежимо довжину URL
            print(f"Заголовок: {article['title']}")
