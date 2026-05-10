import telebot
import subprocess
import os
from telebot import types

# ================= НАСТРОЙКИ =================
# Не забудь про НОВЫЙ токен от BotFather!
ADMIN_TOKEN = '8737991876:AAFKzkGN5Eit-vtjGYbUdZZsh12EjFQPibo'

# Список ID, которым разрешено управлять ботом
ALLOWED_USERS = [7987976077, 1618102167] 

DESKTOP_PATH = '/home/lehdev/Desktop' 
# =============================================

bot = telebot.TeleBot(ADMIN_TOKEN)
running_processes = {}

def get_py_files():
    """Ищет все .py файлы на рабочем столе (кроме самого админа)"""
    files = []
    if not os.path.exists(DESKTOP_PATH):
        return []
    for f in os.listdir(DESKTOP_PATH):
        if f.endswith('.py') and f != 'admin_bot.py':
            files.append(f)
    return files

def send_main_menu(chat_id, old_message_id=None):
    """Удаляет старое сообщение и отправляет новое меню"""
    if old_message_id:
        try:
            bot.delete_message(chat_id, old_message_id)
        except Exception:
            pass

    files = get_py_files()
    text = "🚀 *LehDev HOSTING PANEL*\n"
    text += "--------------------------\n"
    
    markup = types.InlineKeyboardMarkup()
    
    if not files:
        text += "❌ Скрипты .py не найдены на рабочем столе."
    else:
        text += "Управление процессами:"
        for file in files:
            is_running = file in running_processes and running_processes[file].poll() is None
            if not is_running and file in running_processes:
                del running_processes[file]
            
            status = "✅ РАБОТАЕТ" if is_running else "🔴 ВЫКЛЮЧЕН"
            btn_text = f"{status} | {file}"
            markup.add(types.InlineKeyboardButton(btn_text, callback_data=f"manage_{file}"))
    
    markup.add(types.InlineKeyboardButton("🔄 Обновить список", callback_data="refresh"))
    
    bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=['start', 'menu'])
def start_cmd(message):
    # Проверка: есть ли ID пользователя в списке разрешенных
    if message.from_user.id not in ALLOWED_USERS: 
        bot.send_message(message.chat.id, "🚫 Доступ запрещен.")
        return
    send_main_menu(message.chat.id)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    # Проверка прав для кнопок
    if call.from_user.id not in ALLOWED_USERS: 
        bot.answer_callback_query(call.id, "У вас нет прав!", show_alert=True)
        return

    if call.data == "refresh":
        send_main_menu(call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(call.id, "Список обновлен")
        return

    if call.data.startswith("manage_"):
        filename = call.data.replace("manage_", "")
        file_path = os.path.join(DESKTOP_PATH, filename)
        
        is_running = filename in running_processes and running_processes[filename].poll() is None
        
        if is_running:
            running_processes[filename].terminate()
            del running_processes[filename]
            bot.answer_callback_query(call.id, f"🛑 {filename} остановлен")
        else:
            try:
                python_path = os.path.join(DESKTOP_PATH, 'venv', 'bin', 'python3')
                if not os.path.exists(python_path):
                    python_path = 'python3'
                
                proc = subprocess.Popen([python_path, file_path])
                running_processes[filename] = proc
                bot.answer_callback_query(call.id, f"⚡ {filename} запущен")
            except Exception as e:
                bot.send_message(call.message.chat.id, f"❌ Ошибка запуска {filename}: {e}")
        
        send_main_menu(call.message.chat.id, call.message.message_id)

print("LehDev Хостинг запущен для двоих админов!")
bot.polling(none_stop=True)
