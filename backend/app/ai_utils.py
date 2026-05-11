import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
GEMINI_TIMEOUT_MS = int(os.getenv("GEMINI_TIMEOUT_MS", "15000"))
MAX_INPUT_CHARS = int(os.getenv("GEMINI_MAX_INPUT_CHARS", "12000"))

if GEMINI_API_KEY:
    client = genai.Client(
        api_key=GEMINI_API_KEY,
        http_options=types.HttpOptions(timeout=GEMINI_TIMEOUT_MS),
    )
else:
    client = None
    print("ВНИМАНИЕ: API ключ Gemini не найден!")


def process_news_text(raw_text):
    if not client or not raw_text or len(raw_text.strip()) < 20:
        return raw_text

    cleaned_raw_text = raw_text.strip()

    if len(cleaned_raw_text) > MAX_INPUT_CHARS:
        cleaned_raw_text = cleaned_raw_text[:MAX_INPUT_CHARS]

    prompt = (
        "Ты профессиональный редактор новостей. Твоя задача:\n"
        "1. Очистить текст от технического мусора.\n"
        "2. Переписать текст так, чтобы его было легко читать.\n"
        "3. Ограничить объем до 2-3 емких предложений.\n"
        "Верни только обработанный текст."
    )

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=f"{prompt}\n\nТекст: {cleaned_raw_text}",
        )

        if response and getattr(response, "text", None):
            processed_text = response.text.strip()
            return processed_text if processed_text else raw_text

        return raw_text

    except Exception as e:
        print(f"Ошибка при работе с Gemini. Используем исходный текст. Детали: {type(e).__name__}: {e}")
        return raw_text