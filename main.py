import os
import logging
from telegram.ext import Updater, CommandHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.environ["TELEGRAM_TOKEN"]

def start(update, context):
    update.message.reply_text("✅ Бот работает!")

def main():
    updater = Updater(TOKEN, use_context=True)
    updater.dispatcher.add_handler(CommandHandler("start", start))

    logger.info("Бот запущен")
    updater.start_polling()

    # Держим сервер
    from http.server import HTTPServer, BaseHTTPRequestHandler
    import threading

    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")

    port = int(os.environ.get("PORT", 8080))
    s = HTTPServer(('0.0.0.0', port), H)
    threading.Thread(target=s.serve_forever, daemon=True).start()

    updater.idle()

if __name__ == "__main__":
    main()
