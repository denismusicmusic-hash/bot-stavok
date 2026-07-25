import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ========= ТОКЕН ИЗ ПЕРЕМЕННОЙ ОКРУЖЕНИЯ =========
TOKEN = os.environ.get("TELEGRAM_TOKEN")  # Создадим позже

# ========= НАСТРОЙКИ =========
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ========= КОМАНДЫ =========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Привет, {user.first_name}!\n\n"
        f"Я бот для поиска ценных ставок ⚽\n"
        f"Работаю на сервере 24/7 🚀\n\n"
        f"📋 Команды:\n"
        f"🔹 /today - ставки на сегодня\n"
        f"🔹 /help - помощь"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 **Как я работаю:**\n\n"
        "1️⃣ Анализирую статистику команд (xG и т.д.)\n"
        "2️⃣ Сравниваю с коэффициентами букмекеров\n"
        "3️⃣ Нахожу ставки с перевесом (Value > 5%)\n\n"
        "💰 **Рекомендации:**\n"
        "• Ставка: 1-2% от банка\n"
        "• Дистанция: минимум 50 ставок\n"
        "• Умножаем банк, а не удваиваем\n\n"
        "⚡ **Типы ставок:**\n"
        "• Тоталы (больше/меньше)\n"
        "• Обе забьют (ДА/НЕТ)\n"
        "• Победа команды\n"
        "• Форы"
    )

async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Демо-ставки (заменим позже на реальные)
    message = "📊 **СТАВКИ НА СЕГОДНЯ**\n\n"

    message += "═══════════════════════\n"
    message += "🏆 **АПЛ**\n"
    message += "⚽ Ливерпуль vs Арсенал\n"
    message += "🎯 Тотал больше 2.5\n"
    message += "💰 Кэф: 2.10\n"
    message += "📈 Value: +12.5%\n"
    message += "🟢 Уровень: **ВЫСОКИЙ**\n"
    message += "💡 Ставка: 2% от банка\n"
    message += "═══════════════════════\n\n"

    message += "🏆 **Ла Лига**\n"
    message += "⚽ Барселона vs Реал Мадрид\n"
    message += "🎯 Тотал больше 3.5\n"
    message += "💰 Кэф: 3.20\n"
    message += "📈 Value: +8.3%\n"
    message += "🟡 Уровень: **СРЕДНИЙ**\n"
    message += "💡 Ставка: 1.5% от банка\n"
    message += "═══════════════════════\n\n"

    message += "🏆 **Бундеслига**\n"
    message += "⚽ Бавария vs Боруссия\n"
    message += "🎯 Обе забьют - ДА\n"
    message += "💰 Кэф: 1.80\n"
    message += "📈 Value: +6.7%\n"
    message += "🟢 Уровень: **НИЗКИЙ**\n"
    message += "💡 Ставка: 1% от банка\n"
    message += "═══════════════════════\n\n"

    message += "⚠️ **Это демо-версия**\n"
    message += "🔜 Реальные ставки появятся после подключения API!"

    await update.message.reply_text(message)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "ставк" in text or "прогноз" in text:
        await update.message.reply_text("📊 Напиши /today для просмотра ставок на сегодня!")
    elif "привет" in text or "здравствуй" in text:
        await update.message.reply_text("👋 Привет! Используй /help чтобы узнать команды")
    elif "статистик" in text:
        await update.message.reply_text("📊 Статистика скоро будет доступна! Следи за обновлениями")
    else:
        await update.message.reply_text("🤖 Я знаю команды: /start, /help, /today")

# ========= ЗАПУСК =========
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("today", today))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    port = os.environ.get("PORT", 8080)
    print(f"🤖 Бот запущен на порту {port}")
    app.run_polling()

if __name__ == "__main__":
    main()
