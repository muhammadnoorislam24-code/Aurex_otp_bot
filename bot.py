import logging
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    BotCommand,
)
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# =========================================================
# AUREX NOO'R — TELEGRAM BOT PRO
# =========================================================

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger("AurexNoor")

BOT_TOKEN = os.getenv("BOT_TOKEN")
FIVESIM_API_KEY = os.getenv("FIVESIM_API_KEY")

TIKTOK_URL = "https://www.tiktok.com/@aurex_noor1"
YOUTUBE_URL = "https://www.youtube.com/@ToonovaCartoon1"

# Temporary RAM storage
user_data_store = {}


# =========================================================
# USER DATA
# =========================================================

def get_user_data(user_id):
    if user_id not in user_data_store:
        user_data_store[user_id] = {
            "language": "bn",
            "history": [],
            "referrals": 0,
            "referral_earnings": 0.0,
            "balance": 0.0,
            "referred_by": None,
        }

    return user_data_store[user_id]


# =========================================================
# TRANSLATIONS
# =========================================================

TEXTS = {

    "bn": {
        "welcome":
            "👑 *WELCOME TO AUREX NOO'R* 👑\n\n"
            "🚀 আপনার Aurex Noo'R Bot প্রস্তুত।\n\n"
            "📱 GET NUMBER — Service ও Country নির্বাচন করুন।\n"
            "👤 PROFILE — আপনার Profile দেখুন।\n"
            "🎁 REFER — Referral link ও সংখ্যা দেখুন।\n"
            "💰 WITHDRAW — Withdrawal status দেখুন।",

        "get_number":
            "📱 *GET NUMBER*\n\n"
            "নিচের একটি Service নির্বাচন করুন:",

        "profile":
            "👤 *YOUR PROFILE*\n\n"
            "🆔 User ID: `{user_id}`\n"
            "💰 Balance: ${balance:.2f}\n"
            "👥 Total Referrals: {referrals}\n"
            "🎁 Referral Earnings: ${earnings:.2f}",

        "refer":
            "🎁 *REFERRAL PROGRAM*\n\n"
            "👥 আপনার Referral: {referrals}\n"
            "💰 Referral Earnings: ${earnings:.2f}\n\n"
            "🔗 আপনার Referral Link:\n"
            "{link}",

        "withdraw":
            "💰 *WITHDRAW*\n\n"
            "Current Balance: ${balance:.2f}\n\n"
            "Withdrawal system বর্তমানে প্রস্তুত হচ্ছে।",

        "select_service":
            "🛠️ একটি Service নির্বাচন করুন:",

        "select_country":
            "🌍 একটি Country নির্বাচন করুন:",

        "api_unavailable":
            "⚠️ *Service Temporarily Unavailable*\n\n"
            "API configuration সম্পূর্ণ না হওয়া পর্যন্ত Number service চালু করা যাচ্ছে না।",

        "api_configured":
            "✅ API configured আছে।\n\n"
            "Number service integration-এর পরবর্তী ধাপ প্রস্তুত।",

        "menu":
            "⚙️ *AUREX NOO'R MENU*",

        "clear_done":
            "🗑️ আপনার bot-side history সফলভাবে clear করা হয়েছে।",

        "language":
            "🌐 Language নির্বাচন করুন:",

        "language_changed":
            "✅ Language successfully changed.",

        "help":
            "ℹ️ *AUREX NOO'R HELP*\n\n"
            "📱 GET NUMBER — Service ও Country নির্বাচন করুন।\n"
            "👤 PROFILE — আপনার profile দেখুন।\n"
            "🎁 REFER — Referral number ও link দেখুন।\n"
            "💰 WITHDRAW — Withdrawal status দেখুন।\n\n"
            "🌐 Language পরিবর্তন করতে Menu ব্যবহার করুন।\n"
            "🗑️ Bot-side history মুছতে Clear History ব্যবহার করুন।\n\n"
            "⚠️ Password, OTP, 2FA secret বা অন্যের verification code পাঠাবেন না।",

        "back":
            "🔙 Back",

        "closed":
            "Menu closed."
    },

    "en": {
        "welcome":
            "👑 *WELCOME TO AUREX NOO'R* 👑\n\n"
            "🚀 Your Aurex Noo'R Bot is ready.\n\n"
            "📱 GET NUMBER — Select a service and country.\n"
            "👤 PROFILE — View your profile.\n"
            "🎁 REFER — View referrals and link.\n"
            "💰 WITHDRAW — Check withdrawal status.",

        "get_number":
            "📱 *GET NUMBER*\n\n"
            "Select a service:",

        "profile":
            "👤 *YOUR PROFILE*\n\n"
            "🆔 User ID: `{user_id}`\n"
            "💰 Balance: ${balance:.2f}\n"
            "👥 Total Referrals: {referrals}\n"
            "🎁 Referral Earnings: ${earnings:.2f}",

        "refer":
            "🎁 *REFERRAL PROGRAM*\n\n"
            "👥 Referrals: {referrals}\n"
            "💰 Referral Earnings: ${earnings:.2f}\n\n"
            "🔗 Your Referral Link:\n"
            "{link}",

        "withdraw":
            "💰 *WITHDRAW*\n\n"
            "Current Balance: ${balance:.2f}\n\n"
            "Withdrawal system is currently being prepared.",

        "select_service":
            "🛠️ Select a service:",

        "select_country":
            "🌍 Select a country:",

        "api_unavailable":
            "⚠️ *Service Temporarily Unavailable*\n\n"
            "Number service is unavailable until API configuration is completed.",

        "api_configured":
            "✅ API is configured.\n\n"
            "Number service integration is ready for the next step.",

        "menu":
            "⚙️ *AUREX NOO'R MENU*",

        "clear_done":
            "🗑️ Your bot-side history has been cleared.",

        "language":
            "🌐 Select your language:",

        "language_changed":
            "✅ Language successfully changed.",

        "help":
            "ℹ️ *AUREX NOO'R HELP*\n\n"
            "📱 GET NUMBER — Select a service and country.\n"
            "👤 PROFILE — View your profile.\n"
            "🎁 REFER — View referral number and link.\n"
            "💰 WITHDRAW — Check withdrawal status.\n\n"
            "🌐 Change language from Menu.\n"
            "🗑️ Use Clear History to clear bot-side history.\n\n"
            "⚠️ Never send passwords, OTPs, 2FA secrets, or someone else's verification codes.",

        "back":
            "🔙 Back",

        "closed":
            "Menu closed."
    },

    "hi": {
        "welcome":
            "👑 *WELCOME TO AUREX NOO'R* 👑\n\n"
            "🚀 आपका Aurex Noo'R Bot तैयार है।\n\n"
            "📱 GET NUMBER — Service और Country चुनें।\n"
            "👤 PROFILE — अपना Profile देखें।\n"
            "🎁 REFER — Referral link और संख्या देखें।\n"
            "💰 WITHDRAW — Withdrawal status देखें।",

        "get_number":
            "📱 *GET NUMBER*\n\n"
            "एक Service चुनें:",

        "profile":
            "👤 *YOUR PROFILE*\n\n"
            "🆔 User ID: `{user_id}`\n"
            "💰 Balance: ${balance:.2f}\n"
            "👥 Total Referrals: {referrals}\n"
            "🎁 Referral Earnings: ${earnings:.2f}",

        "refer":
            "🎁 *REFERRAL PROGRAM*\n\n"
            "👥 Referrals: {referrals}\n"
            "💰 Referral Earnings: ${earnings:.2f}\n\n"
            "🔗 आपका Referral Link:\n"
            "{link}",

        "withdraw":
            "💰 *WITHDRAW*\n\n"
            "Current Balance: ${balance:.2f}\n\n"
            "Withdrawal system अभी तैयार किया जा रहा है।",

        "select_service":
            "🛠️ एक Service चुनें:",

        "select_country":
            "🌍 एक Country चुनें:",

        "api_unavailable":
            "⚠️ *Service Temporarily Unavailable*\n\n"
            "API configuration पूरा होने तक Number service उपलब्ध नहीं है।",

        "api_configured":
            "✅ API configured है।\n\n"
            "Number service integration अगले चरण के लिए तैयार है।",

        "menu":
            "⚙️ *AUREX NOO'R MENU*",

        "clear_done":
            "🗑️ आपकी bot-side history clear कर दी गई है।",

        "language":
            "🌐 अपनी भाषा चुनें:",

        "language_changed":
            "✅ Language successfully changed.",

        "help":
            "ℹ️ *AUREX NOO'R HELP*\n\n"
            "📱 GET NUMBER — Service और Country चुनें।\n"
            "👤 PROFILE — अपना profile देखें।\n"
            "🎁 REFER — Referral number और link देखें।\n"
            "💰 WITHDRAW — Withdrawal status देखें।\n\n"
            "🌐 Language बदलने के लिए Menu का उपयोग करें।\n"
            "🗑️ Bot-side history हटाने के लिए Clear History का उपयोग करें।\n\n"
            "⚠️ Password, OTP, 2FA secret या किसी अन्य व्यक्ति का verification code न भेजें।",

        "back":
            "🔙 Back",

        "closed":
            "Menu closed."
    }
}


def t(user_id, key, **kwargs):
    data = get_user_data(user_id)
    lang = data.get("language", "bn")

    text = TEXTS.get(lang, TEXTS["bn"]).get(key, key)

    try:
        return text.format(**kwargs)
    except Exception:
        return text


# =========================================================
# KEYBOARDS
# =========================================================

def main_keyboard():
    return ReplyKeyboardMarkup(
        [
            ["📱 GET NUMBER", "👤 PROFILE"],
            ["🎁 REFER", "💰 WITHDRAW"],
        ],
        resize_keyboard=True,
    )


def start_gate_keyboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🎵 TikTok",
                    url=TIKTOK_URL
                )
            ],
            [
                InlineKeyboardButton(
                    "▶️ YouTube",
                    url=YOUTUBE_URL
                )
            ],
            [
                InlineKeyboardButton(
                    "🚀 OPEN BOT",
                    callback_data="open_bot"
                )
            ],
        ]
    )


def menu_keyboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🗑️ Clear History",
                    callback_data="clear_history"
                )
            ],
            [
                InlineKeyboardButton(
                    "🌐 Language",
                    callback_data="language"
                )
            ],
            [
                InlineKeyboardButton(
                    "ℹ️ Help",
                    callback_data="help"
                )
            ],
            [
                InlineKeyboardButton(
                    "❌ Close",
                    callback_data="close"
                )
            ],
        ]
    )


def language_keyboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🇧🇩 বাংলা",
                    callback_data="lang_bn"
                )
            ],
            [
                InlineKeyboardButton(
                    "🇬🇧 English",
                    callback_data="lang_en"
                )
            ],
            [
                InlineKeyboardButton(
                    "🇮🇳 हिन्दी",
                    callback_data="lang_hi"
                )
            ],
            [
                InlineKeyboardButton(
                    "🔙 Back",
                    callback_data="back_menu"
                ),
            ],
        ]
    )


def services_keyboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📘 FB-PC-CLONE",
                    callback_data="service_fbpc"
                )
            ],
            [
                InlineKeyboardButton(
                    "📸 Instagram",
                    callback_data="service_instagram"
                )
            ],
            [
                InlineKeyboardButton(
                    "🆕 Fb-New ID",
                    callback_data="service_fbnew"
                )
            ],
            [
                InlineKeyboardButton(
                    "💬 WhatsApp",
                    callback_data="service_whatsapp"
                )
            ],
        ]
    )


def countries_keyboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🇮🇳 India",
                    callback_data="country_india"
                ),
                InlineKeyboardButton(
                    "🇧🇩 Bangladesh",
                    callback_data="country_bangladesh"
                ),
            ],
            [
                InlineKeyboardButton(
                    "🇸🇦 Saudi Arabia",
                    callback_data="country_saudi"
                ),
                InlineKeyboardButton(
                    "🇲🇱 Mali",
                    callback_data="country_mali"
                ),
            ],
            [
                InlineKeyboardButton(
                    "🇲🇬 Madagascar",
                    callback_data="country_madagascar"
                ),
                InlineKeyboardButton(
                    "🇸🇱 Sierra Leone",
                    callback_data="country_sierra"
                ),
            ],
        ]
    )


# =========================================================
# START
# =========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message:
        return

    user = update.effective_user

    if not user:
        return

    user_id = user.id
    user_data = get_user_data(user_id)

    # Referral processing
    if context.args:

        try:
            referrer_id = int(context.args[0])

            if (
                referrer_id != user_id
                and user_data.get("referred_by") is None
            ):

                referrer = get_user_data(referrer_id)

                user_data["referred_by"] = referrer_id
                referrer["referrals"] += 1

                logger.info(
                    f"Referral added: {referrer_id} -> {user_id}"
                )

        except (ValueError, TypeError):
            pass

    logger.info(
        f"/start received from user {user_id}"
    )

    text = (
        "👑 *WELCOME TO AUREX NOO'R* 👑\n\n"
        "🚀 *Premium Telegram Bot*\n\n"
        "🎵 TikTok: @aurex_noor1\n"
        "▶️ YouTube: ToonovaCartoon1\n\n"
        "👇 নিচের *OPEN BOT* button চাপুন।"
    )

    await update.message.reply_text(
        text,
        reply_markup=start_gate_keyboard(),
        parse_mode="Markdown",
    )


# =========================================================
# MENU
# =========================================================

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    await update.message.reply_text(
        t(user_id, "menu"),
        reply_markup=menu_keyboard(),
        parse_mode="Markdown",
    )


# =========================================================
# HELP
# =========================================================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    await update.message.reply_text(
        t(user_id, "help"),
        parse_mode="Markdown",
    )


# =========================================================
# GET NUMBER
# =========================================================

async def show_get_number(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    await update.message.reply_text(
        t(user_id, "get_number"),
        reply_markup=services_keyboard(),
        parse_mode="Markdown",
    )


# =========================================================
# PROFILE
# =========================================================

async def show_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    data = get_user_data(user_id)

    await update.message.reply_text(
        t(
            user_id,
            "profile",
            user_id=user_id,
            balance=data["balance"],
            referrals=data["referrals"],
            earnings=data["referral_earnings"],
        ),
        parse_mode="Markdown",
    )


# =========================================================
# REFER
# =========================================================

async def show_refer(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    data = get_user_data(user_id)

    bot_username = context.bot.username

    link = f"https://t.me/{bot_username}?start={user_id}"

    await update.message.reply_text(
        t(
            user_id,
            "refer",
            referrals=data["referrals"],
            earnings=data["referral_earnings"],
            link=link,
        ),
        parse_mode="Markdown",
    )


# =========================================================
# WITHDRAW
# =========================================================

async def show_withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    data = get_user_data(user_id)

    await update.message.reply_text(
        t(
            user_id,
            "withdraw",
            balance=data["balance"],
        ),
        parse_mode="Markdown",
    )


# =========================================================
# MESSAGE HANDLER
# =========================================================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message:
        return

    user_id = update.effective_user.id
    text = update.message.text

    if text == "📱 GET NUMBER":

        await show_get_number(update, context)

    elif text == "👤 PROFILE":

        await show_profile(update, context)

    elif text == "🎁 REFER":

        await show_refer(update, context)

    elif text == "💰 WITHDRAW":

        await show_withdraw(update, context)

    else:

        await update.message.reply_text(
            t(user_id, "welcome"),
            reply_markup=main_keyboard(),
            parse_mode="Markdown",
        )


# =========================================================
# CALLBACK HANDLER
# =========================================================

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    if not query:
        return

    await query.answer()

    user_id = query.from_user.id
    data = get_user_data(user_id)

    callback = query.data

    # -----------------------------
    # OPEN BOT
    # -----------------------------

    if callback == "open_bot":

        await query.edit_message_text(
            t(user_id, "welcome"),
            parse_mode="Markdown",
        )

        await query.message.reply_text(
            "👇 Main Menu",
            reply_markup=main_keyboard(),
        )

        return

    # -----------------------------
    # CLEAR HISTORY
    # -----------------------------

    if callback == "clear_history":

        data["history"] = []

        await query.edit_message_text(
            t(user_id, "clear_done")
        )

        return

    # -----------------------------
    # LANGUAGE
    # -----------------------------

    if callback == "language":

        await query.edit_message_text(
            t(user_id, "language"),
            reply_markup=language_keyboard(),
        )

        return

    # -----------------------------
    # LANGUAGE CHANGE
    # -----------------------------

    if callback.startswith("lang_"):

        lang = callback.replace("lang_", "")

        if lang in ("bn", "en", "hi"):
            data["language"] = lang

        await query.edit_message_text(
            t(user_id, "language_changed")
        )

        return

    # -----------------------------
    # HELP
    # -----------------------------

    if callback == "help":

        await query.edit_message_text(
            t(user_id, "help"),
            parse_mode="Markdown",
        )

        return

    # -----------------------------
    # CLOSE
    # -----------------------------

    if callback == "close":

        await query.edit_message_text(
            t(user_id, "closed")
        )

        return

    # -----------------------------
    # BACK TO MENU
    # -----------------------------

    if callback == "back_menu":

        await query.edit_message_text(
            t(user_id, "menu"),
            reply_markup=menu_keyboard(),
            parse_mode="Markdown",
        )

        return

    # -----------------------------
    # SERVICE
    # -----------------------------

    if callback.startswith("service_"):

        service = callback.replace("service_", "")

        data["history"].append(
            {
                "type": "service",
                "service": service,
            }
        )

        await query.edit_message_text(
            t(user_id, "select_country"),
            reply_markup=countries_keyboard(),
            parse_mode="Markdown",
        )

        return

    # -----------------------------
    # COUNTRY
    # -----------------------------

    if callback.startswith("country_"):

        country = callback.replace("country_", "")

        data["history"].append(
            {
                "type": "country",
                "country": country,
            }
        )

        if not FIVESIM_API_KEY:

            await query.edit_message_text(
                t(user_id, "api_unavailable"),
                parse_mode="Markdown",
            )

            return

        await query.edit_message_text(
            t(user_id, "api_configured"),
            parse_mode="Markdown",
        )

        return


# =========================================================
# ERROR HANDLER
# =========================================================

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):

    logger.exception(
        "Unhandled exception:",
        exc_info=context.error,
    )


# =========================================================
# TELEGRAM COMMANDS
# =========================================================

async def post_init(application):

    await application.bot.set_my_commands(
        [
            BotCommand("start", "🚀 Start Bot"),
            BotCommand("menu", "⚙️ Menu"),
            BotCommand("help", "ℹ️ Help"),
        ]
    )

    logger.info("Telegram commands registered successfully.")


# =========================================================
# RENDER HEALTH CHECK
# =========================================================

class HealthCheckHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "text/plain"
        )

        self.end_headers()

        self.wfile.write(
            b"Aurex Noo'R Bot is live and healthy!"
        )

    def log_message(self, format, *args):
        return


def run_health_check():

    port = int(
        os.environ.get(
            "PORT",
            "8080"
        )
    )

    server = HTTPServer(
        ("0.0.0.0", port),
        HealthCheckHandler
    )

    logger.info(
        f"Health check running on port {port}"
    )

    server.serve_forever()


# =========================================================
# MAIN
# =========================================================

def main():

    logger.info("======================================")
    logger.info("Aurex Noo'R Bot is starting...")
    logger.info("======================================")

    if not BOT_TOKEN:

        logger.error(
            "BOT_TOKEN environment variable is missing!"
        )

        return

    # Render health server
    health_thread = threading.Thread(
        target=run_health_check,
        daemon=True
    )

    health_thread.start()

    # Telegram application
    application = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    # Commands
    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("menu", menu)
    )

    application.add_handler(
        CommandHandler("help", help_command)
    )

    # Buttons
    application.add_handler(
        CallbackQueryHandler(handle_callback)
    )

    # Main keyboard
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    application.add_error_handler(
        error_handler
    )

    logger.info(
        "Aurex Noo'R Bot is now polling Telegram..."
    )

    application.run_polling(
        drop_pending_updates=True
    )


# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":
    main()
