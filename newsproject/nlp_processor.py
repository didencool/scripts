%%writefile nlp_processor.py

from langdetect import detect
from typing import List, Dict

# Тимчасові функції без моделей для тестування імпорту

def detect_language(text: str) -> str:
    """Визначає мову тексту, захищаючи від помилок."""
    if not text:
        return 'unknown'
    try:
        # Для тестування зменшимо кількість тексту для langdetect
        return detect(text[:200])
    except:
        return 'unknown'


def translate_to_uk(article: Dict) -> Dict:
    """Тимчасовий переклад без завантаження моделі."""
    title = article.get('title', '')
    lang_code = detect_language(title)
    article['lang'] = lang_code

    if lang_code == 'uk':
        article['ukr_title'] = title
        return article

    article['ukr_title'] = f"[Тимчасовий переклад з {lang_code}]: {title}"
    return article
