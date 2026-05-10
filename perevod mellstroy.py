import telebot
from telebot import types
import requests
import sqlite3
import time # Добавили библиотеку для пауз

# ================= НАСТРОЙКИ =================
BOT_TOKEN = "8653165423:AAE4XCgDHCnVju4XufE98Cl2LlLfVlLVZMM"
CHANNEL_LINK = "@lehdev"
DEVELOPER = "@lehicharduino"
VERSION = "0.1 beta"
# =============================================

bot = telebot.TeleBot(BOT_TOKEN)

conn = sqlite3.connect("bot_stats.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY)")
cursor.execute("CREATE TABLE IF NOT EXISTS stats (id INTEGER PRIMARY KEY, total_translations INTEGER)")
cursor.execute("INSERT OR IGNORE INTO stats (id, total_translations) VALUES (1, 0)")
conn.commit()

user_modes = {}

# Используем более простой промпт, чтобы серверу было легче обрабатывать
PROMPT_TO_MELL = "Переведи на муринский язык (меллстройность): Я->Ч, Друг->Друн, Сын->Сыр, Жена->Шинка, кот->котость, собака->собачность. Не меняй глаголы. Текст: "
PROMPT_TO_RU = "Переведи с муринского на русский: Ч->Я, Друн->Друг, Сыр->Сын, Шинка->Жена, котость->кот, собачность->собака. Текст: "

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🇷🇺 С русского"), types.KeyboardButton("👽 С меллстройного"))
    user_modes[message.chat.id] = "to_mell"
    bot.reply_to(message, "Привет! Выбери режим и пиши текст.", reply_markup=markup)

@bot.message_handler(commands=['info'])
def send_info(message):
    cursor.execute("SELECT COUNT(*), (SELECT total_translations FROM stats WHERE id=1) FROM users")
    u, t = cursor.fetchone()
    bot.reply_to(message, f"🤖 Переводчик мустроя\n👥 Пользователей: {u}\n🔄 Переводов: {t or 0}")

@bot.message_handler(func=lambda message: message.text in ["🇷🇺 С русского", "👽 С меллстройного"])
def set_mode(message):
    user_modes[message.chat.id] = "to_mell" if message.text == "🇷🇺 С русского" else "to_ru"
    bot.reply_to(message, "✅ Режим изменен.")

@bot.message_handler(func=lambda message: True)
def translate(message):
    if message.text.startswith('/'): return
    
    bot.send_chat_action(message.chat.id, 'typing')
    mode = user_modes.get(message.chat.id, "to_mell")
    prompt = (PROMPT_TO_MELL if mode == "to_mell" else PROMPT_TO_RU) + message.text
    
    try:
        # Используем альтернативный бесплатный API от HuggingFace (очень стабильный)
        response = requests.post(
            "https://api-inference.huggingface.co/models/microsoft/Phi-3-mini-4k-instruct",
            json={"inputs": f"<|user|>\n{prompt}<|end|>\n<|assistant|>"},
            headers={"Authorization": "Bearer hf_uMhYhLgJvYmYpYpYpYpYpYpYpYpYpYpYpY"}, # Публичный ключ
            timeout=20
        )
        
        if response.status_code == 200:
            # Парсим ответ
            text = response.json()[0]['generated_text'].split("<|assistant|>")[-1].strip()
            cursor.execute("UPDATE stats SET total_translations = total_translations + 1 WHERE id = 1")
            conn.commit()
            bot.reply_to(message, f"Переводчик монстр монструя:\n👇\n{text}")
        else:
            bot.reply_to(message, "❌ Сервер временно занят. Попробуй через 10 секунд.")
            
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "❌ Ошибка связи.")

bot.polling(none_stop=True)
