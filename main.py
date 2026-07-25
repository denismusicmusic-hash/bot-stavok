import logging
import os
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# ========= ТОКЕН =========
TOKEN = os.environ.get("TELEGRAM_TOKEN")

# ========= НАСТРОЙКИ =========
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ========= ОБРАБОТЧИКИ =========
def start(update: Update, context: CallbackContext):
    user = update.effective_user
    logger.info(f"Пользователь {user.first_name} запустил бота")
    update.message.reply_text(
        f"👋 Привет, {user.first_name}!\n\n"
        f"Я бот для поиска ценных ставок ⚽\n"
        f"Работаю 24/7 на сервере 🚀\n\n"
        f"📋 Команды:\n"
        f"🔹 /today - ставки на сегодня\n"
        f"🔹 /help - помощь"
    )

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🤖 **Как я работаю:**\n\n"
        "1️⃣ Анализирую статистику команд\n"
        "2️⃣ Сравниваю с коэффициентами букмекеров\n"
        "3️⃣ Нахожу ставки с перевесом\n\n"
        "💰 **Рекомендации:**\n"
        "• Ставка: 1-2% от банка\n"
        "• Дистанция: минимум 50 ставок\n\n"
        "📋 **Команды:**\n"
        "• /start - начать\n"
        "• /today - ставки на сегодня\n"
        "• /help - эта справка"
    )

def today(update: Update, context: CallbackContext):
    message = "📊 **СТАВКИ НА СЕГОДНЯ**\n\n"

    message += "═══════════════════════\n"
    message += "🏆 **АПЛ**\n"
    message += "⚽ Ливерпуль vs Арсенал\n"
    message += "🎯 Тотал больше 2.5\n"
    message += "💰 Кэф: 2.10 | Value: +12.5%\n"
    message += "🟢 Уровень: **ВЫСОКИЙ**\n"
    message += "═══════════════════════\n\n"

    message += "🏆 **Ла Лига**\n"
    message += "⚽ Барселона vs Реал Мадрид\n"
    message += "🎯 Тотал больше 3.5\n"
    message += "💰 Кэф: 3.20 | Value: +8.3%\n"
    message += "🟡 Уровень: **СРЕДНИЙ**\n"
    message += "═══════════════════════\n\n"

    message += "🏆 **Бундеслига**\n"
    message += "⚽ Бавария vs Боруссия\n"
    message += "🎯 Обе забьют - ДА\n"
    message += "💰 Кэф: 1.80 | Value: +6.7%\n"
    message += "🟢 Уровень: **НИЗКИЙ**\n"
    message += "═══════════════════════\n\n"

    message += "⚠️ Демо-версия\n"
    message += "🔜 Реальные ставки скоро!"

    update.message.reply_text(message)

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text.lower()

    if "ставк" in text or "прогноз" in text:
        update.message.reply_text("📊 Напиши /today для ставок!")
    elif "привет" in text:
        update.message.reply_text("👋 Привет! Используй /help")
    else:
        update.message.reply_text("🤖 Я знаю: /start, /help, /today")

def error_handler(update: Update, context: CallbackContext):
    """Логирование ошибок"""
    logger.error(f"Update {update} caused error {context.error}")

# ========= ГЛАВНАЯ ФУНКЦИЯ =========
def main():
    """Запуск бота"""
    try:
        # Создаём Updater
        updater = Updater(TOKEN, use_context=True)
        dp = updater.dispatcher

        # Добавляем обработчики
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", help_command))
        dp.add_handler(CommandHandler("today", today))
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
        dp.add_error_handler(error_handler)

        logger.info("🤖 Бот успешно запущен!")

        # Запускаем
        updater.start_polling()

        # Держим сервер живым
        from http.server import HTTPServer, BaseHTTPRequestHandler

        class SimpleHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"Bot is running!")

        port = int(os.environ.get("PORT", 8080))
        server = HTTPServer(('0.0.0.0', port), SimpleHandler)
        logger.info(f"HTTP сервер запущен на порту {port}")

        # Держим работающим
        import threading
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        # Ждём завершения
        updater.idle()

    except Exception as e:
        logger.error(f"❌ Ошибка при запуске: {e}")

# ========= ТОЧКА ВХОДА =========
if __name__ == "__main__":
    main()
