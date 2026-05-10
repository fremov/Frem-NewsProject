from deep_translator import GoogleTranslator

def translate_to_russian(text):
    if not text or len(text.strip()) == 0:
        return ""
    try:
        # GoogleTranslator автоматически обрабатывает длинные тексты
        return GoogleTranslator(source='en', target='ru').translate(text)
    except Exception as e:
        print(f"Ошибка перевода: {e}")
        return text