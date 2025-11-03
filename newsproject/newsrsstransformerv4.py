import feedparser
from typing import List, Dict
from langdetect import detect
from transformers import pipeline

# ==========================================================
# 1. ІНІЦІАЛІЗАЦІЯ МОДЕЛЕЙ
# ==========================================================

# Модель для англійської -> української
EN_UK_TRANSLATOR = pipeline(
    "translation", 
    model="Helsinki-NLP/opus-mt-en-uk"
)
# Модель для російської -> української
RU_UK_TRANSLATOR = pipeline(
    "translation", 
    model="Helsinki-NLP/opus-mt-ru-uk" 
)

# ==========================================================
# 2. ФУНКЦІЇ ДЕТЕКТУВАННЯ ТА ПЕРЕКЛАДУ (Перевірте, чи є вони у вашому коді)
# ==========================================================

def detect_language(text: str) -> str:
    # ... (функція detect_language з langdetect) ...
    if not text:
        return 'unknown'
    try:
        from langdetect import detect
        return detect(text[:200])
    except:
        return 'unknown'


def translate_to_uk(text: str, lang_code: str) -> str:
    """Використовує відповідну модель для перекладу на українську."""
    
    if lang_code == 'uk':
        return text  # Якщо вже українська, повертаємо оригінал
    
    try:
        if lang_code == 'en':
            translator = EN_UK_TRANSLATOR
            
        elif lang_code == 'ru':
            translator = RU_UK_TRANSLATOR
            
        else:
            # Для непідтримуваних мов (наприклад, de, fr)
            return f"[Не перекладено з {lang_code}: {text}]"

        # Виконуємо переклад
        result = translator(text, max_length=150)
        return result[0]['translation_text']
        
    except Exception as e:
        print(f"Помилка перекладу {lang_code}->UK: {e}")
        return f"[Помилка перекладу: {text}]"


def process_and_translate_news(collected_articles: List[Dict]) -> List[Dict]:
    """Визначає мову, перекладає на українську і додає нове поле 'ukr_title'."""
    print(f"\nРозпочато визначення мови та переклад для {len(collected_articles)} новин...")
    translated_news = []
    
    for i, article in enumerate(collected_articles):
        title = article.get('title', '')
        
        lang_code = detect_language(title)
        article['lang'] = lang_code
        
        ukr_title = translate_to_uk(title, lang_code)
        article['ukr_title'] = ukr_title
        
        translated_news.append(article)
        
        if (i + 1) % 25 == 0:
            print(f"  Прогрес: оброблено {i+1} новин...")
            
    return translated_news

# ==========================================================
# 3. БЛОК ЗАПУСКУ
# ==========================================================

if __name__ == "__main__":
    # ... [Код load_sources та fetch_news має бути тут] ...

    # Припустимо, NEWS_LIMIT визначено на початку файлу
    
    # 1. Завантаження та збір
    NEWS_SOURCES = load_sources(SOURCES_FILE)
    if NEWS_SOURCES:
        collected_articles = fetch_news(NEWS_SOURCES, NEWS_LIMIT)
        
        # 2. Запуск визначення мови та перекладу
        translated_results = process_and_translate_news(collected_articles)
        
        # 3. Вивід прикладів з перекладом
        print(f"\nПриклади {NEWS_LIMIT} новин з перекладом:")
        for i, article in enumerate(translated_results[:NEWS_LIMIT]):
            print(f"--- Новина {i+1} ---")
            print(f"  Оригінал [{article['lang']}]: {article['title']}")
            print(f"  Переклад [uk]: {article['ukr_title']}")
