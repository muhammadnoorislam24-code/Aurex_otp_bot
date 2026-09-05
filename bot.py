import os
import logging
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# =========================
# Logging
# =========================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# =========================
# Render Health Check
# =========================
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot is live and healthy!")

    def log_message(self, format, *args):
        return


def run_health_check():
    port = int(os.environ.get("PORT", 10000))

    server = HTTPServer(
        ("0.0.0.0", port),
        HealthCheckHandler
    )

    logger.info(f"Health check server running on port {port}")
    server.serve_forever()


# Start health check server
threading.Thread(
    target=run_health_check,
    daemon=True
).start()


# =========================
# Telegram Bot
# =========================
TOKEN = os.environ.get("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello!\n\n"
        "Aurex Noo'R Bot is online and working perfectly! 🤖"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 Available Commands:\n\n"
        "/start - Start the bot\n"
        "/help - Show help"
    )


# =========================
# Main
# =========================
def main():

    if not TOKEN:
        raise RuntimeError(
            "BOT_TOKEN environment variable is missing!"
        )

    app = ApplicationBuilder().token(TOKEN).build()

    # Commands
    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("help", help_command)
    )

    logger.info("Aurex Noo'R Bot is starting...")

    # Start polling
    app.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
