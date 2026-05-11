import os
from google import genai  # Используем актуальный импорт
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Инициализируем клиент правильно
# Для нового SDK (google-genai) лучше использовать такой подход:
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)
else:
    client = None
    print("ВНИМАНИЕ: API ключ Gemini не найден!")


def process_news_text(raw_text):
    if not client or not raw_text or len(raw_text) < 20:
        return raw_text

    prompt = (
        "Ты профессиональный редактор новостей. Твоя задача:\n"
        "1. Очистить текст от технического мусора.\n"
        "2. Переписать текст так, чтобы его было легко читать.\n"
        "3. Ограничить объем до 2-3 емких предложений.\n"
        "Верни только обработанный текст."
    )

    try:
        # 1. Попробуем использовать полное имя модели "models/gemini-1.5-flash"
        # 2. В новом SDK параметры передаются именно так
        response = client.models.generate_content(
            model="models/gemini-1.5-flash",
            contents=f"{prompt}\n\nТекст: {raw_text}"
        )

        # В новом SDK ответ может быть в response.text
        if response and response.text:
            return response.text.strip()
        return raw_text

    except Exception as e:
        # Если снова 404, попробуй поменять модель на "gemini-1.5-flash-latest"
        print(f"Ошибка при работе с Gemini: {e}")
        return raw_text