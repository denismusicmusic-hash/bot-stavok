import logging
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен бота
TOKEN = os.environ.get("TELEGRAM_TOKEN")

def start(update, context):
    """Ответ на команду /start"""
    user = update.effective_user
    update.message.reply_text(
        f"👋 Привет, {user.first_name}!\n"
        f"Бот работает 24/7 🚀\n"
        f"Команды: /help, /today"
    )
    logger.info(f"Пользователь {user.first_name} запустил бота")

def help_command(update, context):
    """Ответ на команду /help"""
    update.message.reply_text(
        "📋 Команды:\n"
        "/start - перезапуск\n"
        "/help - справка\n"
        "/today - ставки на сегодня"
    )

def today(update, context):
    """Ответ на команду /today"""
    update.message.reply_text(
        "📊 Ставки на сегодня:\n\n"
        "⚽ Ливерпуль vs Арсенал\n"
        "🎯 Тотал больше 2.5 | Кэф 2.10\n\n"
        "⚽ Барселона vs Реал\n"
        "🎯 Обе забьют ДА | Кэф 1.80\n\n"
        "⚽ Бавария vs Боруссия\n"
        "🎯 Победа Баварии | Кэф 1.70\n\n"
        "🔜 Скоро реальные коэффициенты!"
    )

def echo(update, context):
    """Ответ на любое сообщение"""
    text = update.message.text
    if "привет" in text.lower():
        update.message.reply_text("Привет! Напиши /help")
    elif "ставк" in text.lower() or "прогноз" in text.lower():
        update.message.reply_text("Напиши /today для просмотра ставок")
    else:
        update.message.reply_text(f"Я не понял. Попробуй /help")

def error(update, context):
    """Логирование ошибок"""
    logger.warning(f"Ошибка: {context.error}")

def main():
    """Запуск бота"""
    try:
        # Создаем updater
        updater = Updater(TOKEN, use_context=True)
        dp = updater.dispatcher

        # Команды
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", help_command))
        dp.add_handler(CommandHandler("today", today))

        # Текстовые сообщения
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

        # Обработчик ошибок
        dp.add_error_handler(error)

        # Запуск
        logger.info("✅ Бот запущен!")
        updater.start_polling()

        # Держим процесс активным
        if os.environ.get("PORT"):
            # Для Render.com - имитируем веб-сервер
            from http.server import HTTPServer, BaseHTTPRequestHandler
            import threading

            class Handler(BaseHTTPRequestHandler):
                def do_GET(self):
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b"Bot is running")

            port = int(os.environ.get("PORT", 8080))
            server = HTTPServer(('0.0.0.0', port), Handler)
            thread = threading.Thread(target=server.serve_forever)
            thread.daemon = True
            thread.start()
            logger.info(f"🌐 Сервер слушает порт {port}")

        updater.idle()

    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")

if __name__ == '__main__':
    main()
