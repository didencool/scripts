# ==========================================================
# 1. ІМПОРТ МОДУЛІВ
# ==========================================================

#from data_loader import load_sources, fetch_news # ТЕПЕР ПРАЦЮЄ
#from nlp_processor import translate_to_uk, detect_language
#from typing import List, Dict

# =======================================================
# АДАПТИВНИЙ ІМПОРТ: дозволяє запускати як модуль (-m) або як скрипт
# =======================================================
if __name__ == "__main__" and __package__ is None:
    # Запуск як звичайний скрипт (наприклад, python __main__.py)
    # Ми тут використовуємо абсолютний імпорт (як це було у вас)
    from data_loader import load_sources, fetch_news
    from nlp_processor import translate_to_uk, detect_language
    from typing import List, Dict
else:
    # Запуск як модуль/пакет (наприклад, python -m scripts.newsproject)
    # Тут потрібен відносний імпорт
    from .data_loader import load_sources, fetch_news
    from .nlp_processor import translate_to_uk, detect_language
    from typing import List, Dict
# =======================================================

# Ваш основний код, який використовує load_sources і fetch_news
if __name__ == "__main__":
    # ... тут ваш основний код програми ...
    print("Код newsproject успішно запущено!")
    # ...

# ==========================================================
# 2. КОНФІГУРАЦІЯ
# ==========================================================
# ЗМІНІТЬ ЦЕЙ ШЛЯХ на ваш реальний!
SOURCES_FILE = "/content/drive/MyDrive/Colab Notebooks/newsrssreader/newsfeed.txt"
NEWS_LIMIT = 5 # Кількість новин на одне джерело

def process_and_analyze_news(articles: List[Dict]) -> List[Dict]:
    """Головний цикл обробки: переклад."""
    processed_articles = []
    print(f"\nРозпочато обробку {len(articles)} новин...")

    for article in articles:
        translated_article = translate_to_uk(article)
        processed_articles.append(translated_article)

    return processed_articles


if __name__ == "__main__":

    # 1. Завантаження джерел
    rss_sources = load_sources(SOURCES_FILE)

    if not rss_sources:
        print("Неможливо продовжити: список джерел порожній.")
    else:
        # 2. Збір новин
        collected_articles = fetch_news(rss_sources, NEWS_LIMIT)

        # 3. Обробка та аналіз
        final_results = process_and_analyze_news(collected_articles)

        # 4. Вивід результатів
        print(f"\nПриклади оброблених новин:")
        for i, article in enumerate(final_results):
            print(f"--- Новина {i+1} ---")
            print(f"  Джерело: {article.get('source', '')[:40]}...")
            print(f"  Оригінал [{article.get('lang', 'N/A')}]: {article.get('title', 'N/A')}")
            print(f"  Переклад [uk]: {article.get('ukr_title', 'N/A')}")
