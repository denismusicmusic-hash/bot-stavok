import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ========= ТОКЕН =========
TOKEN = os.environ.get("8996710618:AAEBYipmbRh6GMz5yqLTrjmr9yXfIVcfFgY")

# ========= НАСТРОЙКИ ЛОГИРОВАНИЯ =========
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ========= ОБРАБОТЧИКИ =========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"Пользователь {user.first_name} запустил бота")
    await update.message.reply_text(
        f"👋 Привет, {user.first_name}!\n\n"
        f"Я бот для поиска ценных ставок ⚽\n"
        f"Работаю 24/7 на сервере 🚀\n\n"
        f"📋 Команды:\n"
        f"🔹 /today - ставки на сегодня\n"
        f"🔹 /help - помощь"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
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

async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    await update.message.reply_text(message)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "ставк" in text or "прогноз" in text:
        await update.message.reply_text("📊 Напиши /today для ставок!")
    elif "привет" in text:
        await update.message.reply_text("👋 Привет! Используй /help")
    else:
        await update.message.reply_text("🤖 Я знаю: /start, /help, /today")

# ========= ГЛАВНАЯ ФУНКЦИЯ =========
def main():
    """Запуск бота"""
    try:
        # Создаём приложение
        app = Application.builder().token(TOKEN).build()

        # Добавляем обработчики
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("today", today))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        logger.info("🤖 Бот успешно запущен!")

        # Запускаем бота
        app.run_polling()

    except Exception as e:
        logger.error(f"❌ Ошибка при запуске: {e}")

# ========= ТОЧКА ВХОДА =========
if __name__ == "__main__":
    main()

