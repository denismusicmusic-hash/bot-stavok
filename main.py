import os
import logging
import threading
from telegram.ext import Updater, CommandHandler
from flask import Flask

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Получаем токен
TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TOKEN:
    logger.error("❌ TELEGRAM_TOKEN не установлен!")
    exit(1)

# Создаем Flask приложение для веб-сервера
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Telegram Bot is running!", 200

@app.route('/health')
def health():
    return "OK", 200

# Функции бота
def start(update, context):
    """Обработчик команды /start"""
    user = update.effective_user
    update.message.reply_text(
        f"🎉 Привет, {user.first_name}!\n"
        f"🤖 Бот успешно запущен!\n"
        f"📍 Сервер: Render.com\n"
        f"📡 Статус: Онлайн 24/7\n\n"
        f"📋 Команды:\n"
        f"• /start - перезапуск\n"
        f"• /today - ставки\n"
        f"• /help - помощь"
    )
    logger.info(f"Пользователь {user.first_name} запустил бота")

def today(update, context):
    """Обработчик команды /today"""
    update.message.reply_text(
        "📊 **СТАВКИ НА СЕГОДНЯ**\n\n"
        "⚽ Ливерпуль vs Арсенал\n"
        "🎯 Тотал больше 2.5\n"
        "💰 Кэф: 2.10\n"
        "🏆 Лига: АПЛ\n\n"
        "⚽ Барселона vs Реал\n"
        "🎯 Обе забьют: ДА\n"
        "💰 Кэф: 1.80\n"
        "🏆 Лига: Ла Лига\n\n"
        "🔥 Скоро реальные аналитика!"
    )

def help_command(update, context):
    """Обработчик команды /help"""
    update.message.reply_text(
        "📋 **СПРАВКА**\n\n"
        "🤖 Я бот для поиска ценных ставок\n"
        "📡 Работаю на сервере Render.com\n\n"
        "📌 **Команды:**\n"
        "• /start - запуск бота\n"
        "• /today - ставки на сегодня\n"
        "• /help - эта справка\n\n"
        "📞 **Техподдержка:**\n"
        "По всем вопросам пиши мне"
    )

def error_handler(update, context):
    """Обработчик ошибок"""
    logger.error(f"Ошибка: {context.error}")

def run_flask():
    """Запуск Flask сервера"""
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=False)

def main():
    """Основная функция"""
    try:
        # Создаем и запускаем Flask в отдельном потоке
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()
        logger.info(f"🌐 Flask сервер запущен на порту {os.environ.get('PORT', 8080)}")

        # Создаем бота
        updater = Updater(TOKEN, use_context=True)
        dp = updater.dispatcher

        # Добавляем обработчики
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("today", today))
        dp.add_handler(CommandHandler("help", help_command))
        dp.add_error_handler(error_handler)

        # Запускаем бота
        logger.info("🤖 Telegram бот запускается...")
        updater.start_polling()
        logger.info("✅ Бот успешно запущен и работает!")

        # Ждем
        updater.idle()

    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")

if __name__ == "__main__":
    main()
