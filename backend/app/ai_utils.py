import os
from google.genai import Client

# Считываем ключ из .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Инициализируем клиент
if GEMINI_API_KEY:
    client = Client(api_key=GEMINI_API_KEY)
else:
    client = None
    print("ВНИМАНИЕ: API ключ Gemini не найден!")

def process_news_text(raw_text):
    if not client or not raw_text or len(raw_text) < 20:
        return raw_text

    prompt = (
        "Ты профессиональный редактор новостей. Твоя задача: "
        "1. Очистить текст от технического мусора. "
        "2. Переписать текст так, чтобы его было легко читать. "
        "3. Ограничить объем до 2-3 емких предложений. "
        "Верни только обработанный текст."
    )

    try:
        # В новом SDK используется метод models.generate_content
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=f"{prompt}\n\nТекст: {raw_text}"
        )
        return response.text.strip()
    except Exception as e:
        print(f"Ошибка нового Gemini SDK: {e}")
        return raw_text