import os
import telebot
from flask import Flask, request

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "my_secret_path")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# --- Главное меню ---
kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
kb.row(telebot.types.KeyboardButton("Текст"), telebot.types.KeyboardButton("Изображения"))
kb.row(telebot.types.KeyboardButton("Видео"), telebot.types.KeyboardButton("Написание кода"))
kb.row(telebot.types.KeyboardButton("Из трендов"))

# --- ТЕКСТ ---
TEXT_INFO = """
1. Yandex GPT
плюсы:
• Глубокое знание русского контекста
• Интеграция в экосистему Яндекса
• Работа с актуальной информацией
минусы:
• Ограниченная память диалога
• Слабость в математике
• Ограничение языков
https://yandex.cloud/en/services/yandexgpt
"""

IMAGE_INFO = """
1. Шедеврум
плюсы:
• Отлично понимает русский язык
• Удобный мобильный формат
• Быстрая генерация
минусы:
• Ограниченные стили
• Средняя детализация
• Требует аккаунт Яндекса
https://shedevrum.ai/
"""

VIDEO_INFO = """
1. Sora 2
плюсы:
• Очень реалистичная генерация видео
• Понимание сложных сцен
• Кинематографичный стиль
минусы:
• Ограниченный доступ
• Высокие требования к запросу
• Возможные ограничения по странам
"""

CODE_INFO = """
1. Cursor AI
плюсы:
• Интеграция с IDE
• Понимание проекта целиком
• Автогенерация и рефакторинг
минусы:
• Платная версия
• Требует мощный ПК
• Возможны ошибки в сложной логике
https://cursor.com/
"""

TREND_INFO = """
🔥 Популярные AI-тренды с DeepSeek
https://www.deepseek.com/en/
"""

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=kb)

@bot.message_handler(func=lambda m: m.text == "Текст")
def text_info(message):
    bot.send_message(message.chat.id, TEXT_INFO)

@bot.message_handler(func=lambda m: m.text == "Изображения")
def image_info(message):
    bot.send_message(message.chat.id, IMAGE_INFO)

@bot.message_handler(func=lambda m: m.text == "Видео")
def video_info(message):
    bot.send_message(message.chat.id, VIDEO_INFO)

@bot.message_handler(func=lambda m: m.text == "Написание кода")
def code_info(message):
    bot.send_message(message.chat.id, CODE_INFO)

@bot.message_handler(func=lambda m: m.text == "Из трендов")
def trend_info(message):
    bot.send_message(message.chat.id, TREND_INFO)

@app.post(f"/webhook/{WEBHOOK_SECRET}")
def webhook():
    json_str = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "ok", 200

@app.get("/")
def index():
    return "Bot is running", 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
bot.infinity_polling()
