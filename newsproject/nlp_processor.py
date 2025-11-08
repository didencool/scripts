from langdetect import detect
from transformers import pipeline
from typing import List, Dict

# ==========================================================
# ІНІЦІАЛІЗАЦІЯ МОДЕЛЕЙ (Це завантажить моделі, коли файл імпортується)
# ==========================================================
# device=0 - вказує використовувати GPU
try:
    EN_UK_TRANSLATOR = pipeline("translation", model="Helsinki-NLP/opus-mt-en-uk", device=0)
    RU_UK_TRANSLATOR = pipeline("translation", model="Helsinki-NLP/opus-mt-ru-uk", device=0)
except Exception as e:
    print(f"Помилка при ініціалізації моделей перекладу: {e}")
    EN_UK_TRANSLATOR = None
    RU_UK_TRANSLATOR = None
# ==========================================================


def detect_language(text: str) -> str:
    """Визначає мову тексту, захищаючи від помилок."""
    if not text:
        return 'unknown'
    try:
        return detect(text[:200])
    except:
        return 'unknown'


def translate_to_uk(article: Dict) -> Dict:
    """Визначає мову та виконує нейромережевий переклад заголовка."""
    
    title = article.get('title', '')
    lang_code = detect_language(title)
    article['lang'] = lang_code
    
    if lang_code == 'uk':
        article['ukr_title'] = title
        return article
        
    try:
        if lang_code == 'en' and EN_UK_TRANSLATOR:
            result = EN_UK_TRANSLATOR(title, max_length=150)
            
        elif lang_code == 'ru' and RU_UK_TRANSLATOR:
            result = RU_UK_TRANSLATOR(title, max_length=150)
            
        else:
            article['ukr_title'] = f"[НЕ ПЕРЕКЛАДЕНО З {lang_code}]: {title}"
            return article

        article['ukr_title'] = result[0]['translation_text']
        
    except Exception as e:
        article['ukr_title'] = f"[ПОМИЛКА ПЕРЕКЛАДУ: {e}]"
        
    return article
