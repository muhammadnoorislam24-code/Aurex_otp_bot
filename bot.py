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
# AUREX NOO'R — PRO VERSION
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
users = {}


# =========================================================
# USER DATA
# =========================================================

def get_user(user_id):
    if user_id not in users:
        users[user_id] = {
            "language": "bn",
            "history": [],
            "referrals": 0,
            "referral_earnings": 0.0,
            "balance": 0.0,
            "referred_by": None,
        }

    return users[user_id]


# =========================================================
# TRANSLATION
# =========================================================

TEXT = {

    "bn": {
        "welcome":
            "👑 *WELCOME TO AUREX NOO'R* 👑\n\n"
            "🚀 *Premium Telegram Bot*\n\n"
            "📱 GET NUMBER — Service ও Country নির্বাচন করুন।\n"
            "🔐 2FA CODE — নিরাপদ 2FA তথ্য দেখুন।\n"
            "👤 PROFILE — আপনার Profile দেখুন।\n"
            "🎁 REFER — Referral link ও সংখ্যা দেখুন।\n"
            "💰 WITHDRAW — Withdrawal status দেখুন।",

        "menu":
            "⚙️ *AUREX NOO'R MENU*",

        "help":
            "ℹ️ *AUREX NOO'R HELP*\n\n"
            "📱 GET NUMBER — Service ও Country নির্বাচন করুন।\n"
            "🔐 2FA CODE — নিরাপদ 2FA সম্পর্কিত তথ্য।\n"
            "👤 PROFILE — আপনার profile দেখুন।\n"
            "🎁 REFER — Referral number ও link দেখুন।\n"
            "💰 WITHDRAW — Withdrawal status দেখুন।\n\n"
            "🌐 Language পরিবর্তন করতে Menu ব্যবহার করুন।\n"
            "🗑️ Clear History ব্যবহার করে bot-side history মুছুন।\n\n"
            "⚠️ Password, OTP, 2FA secret বা অন্যের verification code পাঠাবেন না।",

        "get_number":
            "📱 *GET NUMBER*\n\n"
            "একটি Service নির্বাচন করুন:",

        "select_country":
            "🌍 একটি Country নির্বাচন করুন:",

        "api_unavailable":
            "⚠️ *SERVICE UNAVAILABLE*\n\n"
            "Number service বর্তমানে API configuration-এর জন্য unavailable।\n\n"
            "কোনো fake/random number তৈরি করা হবে না।",

        "profile":
            "👤 *YOUR PROFILE*\n\n"
            "🆔 User ID: `{user_id}`\n"
            "💰 Balance: ${balance:.2f}\n"
            "👥 Total Referrals: {referrals}\n"
            "🎁 Referral Earnings: ${earnings:.2f}",

        "refer":
            "🎁 *REFERRAL PROGRAM*\n\n"
            "👥 Total Referrals: {referrals}\n"
            "💰 Referral Earnings: ${earnings:.2f}\n\n"
            "🔗 *Your Referral Link:*\n"
            "{link}",

        "withdraw":
            "💰 *WITHDRAW*\n\n"
            "💵 Current Balance: ${balance:.2f}\n\n"
            "Withdrawal system বর্তমানে প্রস্তুত করা হচ্ছে।",

        "twofa":
            "🔐 *2FA CODE*\n\n"
            "আপনার নিজের account-এর 2FA security সম্পর্কিত তথ্য এখানে দেখতে পারেন।\n\n"
            "⚠️ কোনো password, OTP, 2FA secret বা verification code এখানে পাঠাবেন না।",

        "clear":
            "🗑️ Bot-side history successfully cleared.",

        "language":
            "🌐 আপনার Language নির্বাচন করুন:",

        "language_changed":
            "✅ Language changed successfully.",

        "closed":
            "Menu closed."
    },

    "en": {
        "welcome":
            "👑 *WELCOME TO AUREX NOO'R* 👑\n\n"
            "🚀 *Premium Telegram Bot*\n\n"
            "📱 GET NUMBER — Select Service and Country.\n"
            "🔐 2FA CODE — View safe 2FA information.\n"
            "👤 PROFILE — View your profile.\n"
            "🎁 REFER — View referral information.\n"
            "💰 WITHDRAW — Check withdrawal status.",

        "menu":
            "⚙️ *AUREX NOO'R MENU*",

        "help":
            "ℹ️ *AUREX NOO'R HELP*\n\n"
            "📱 GET NUMBER — Select Service and Country.\n"
            "🔐 2FA CODE — Safe 2FA information.\n"
            "👤 PROFILE — View your profile.\n"
            "🎁 REFER — View referral number and link.\n"
            "💰 WITHDRAW — Check withdrawal status.\n\n"
            "🌐 Change language from Menu.\n"
            "🗑️ Use Clear History to clear bot-side history.\n\n"
            "⚠️ Never send passwords, OTPs, 2FA secrets, or someone else's verification codes.",

        "get_number":
            "📱 *GET NUMBER*\n\n"
            "Select a Service:",

        "select_country":
            "🌍 Select a Country:",

        "api_unavailable":
            "⚠️ *SERVICE UNAVAILABLE*\n\n"
            "Number service is currently unavailable because API configuration is incomplete.\n\n"
            "No fake or random number will be generated.",

        "profile":
            "👤 *YOUR PROFILE*\n\n"
            "🆔 User ID: `{user_id}`\n"
            "💰 Balance: ${balance:.2f}\n"
            "👥 Total Referrals: {referrals}\n"
            "🎁 Referral Earnings: ${earnings:.2f}",

        "refer":
            "🎁 *REFERRAL PROGRAM*\n\n"
            "👥 Total Referrals: {referrals}\n"
            "💰 Referral Earnings: ${earnings:.2f}\n\n"
            "🔗 *Your Referral Link:*\n"
            "{link}",

        "withdraw":
            "💰 *WITHDRAW*\n\n"
            "💵 Current Balance: ${balance:.2f}\n\n"
            "Withdrawal system is currently being prepared.",

        "twofa":
            "🔐 *2FA CODE*\n\n"
            "You can view safe information about 2FA security for your own account here.\n\n"
            "⚠️ Never send passwords, OTPs, 2FA secrets, or verification codes here.",

        "clear":
            "🗑️ Bot-side history successfully cleared.",

        "language":
            "🌐 Select your language:",

        "language_changed":
            "✅ Language changed successfully.",

        "closed":
            "Menu closed."
    },

    "hi": {
        "welcome":
            "👑 *WELCOME TO AUREX NOO'R* 👑\n\n"
            "🚀 *Premium Telegram Bot*\n\n"
            "📱 GET NUMBER — Service और Country चुनें।\n"
            "🔐 2FA CODE — सुरक्षित 2FA जानकारी देखें।\n"
            "👤 PROFILE — अपना Profile देखें।\n"
            "🎁 REFER — Referral जानकारी देखें।\n"
            "💰 WITHDRAW — Withdrawal status देखें।",

        "menu":
            "⚙️ *AUREX NOO'R MENU*",

        "help":
            "ℹ️ *AUREX NOO'R HELP*\n\n"
            "📱 GET NUMBER — Service और Country चुनें।\n"
            "🔐 2FA CODE — सुरक्षित 2FA जानकारी।\n"
            "👤 PROFILE — अपना profile देखें।\n"
            "🎁 REFER — Referral number और link देखें।\n"
            "💰 WITHDRAW — Withdrawal status देखें।\n\n"
            "🌐 Language बदलने के लिए Menu का उपयोग करें।\n"
            "🗑️ Clear History से bot-side history हटाएँ।\n\n"
            "⚠️ Password, OTP, 2FA secret या किसी अन्य व्यक्ति का verification code न भेजें।",

        "get_number":
            "📱 *GET NUMBER*\n\n"
            "एक Service चुनें:",

        "select_country":
            "🌍 एक Country चुनें:",

        "api_unavailable":
            "⚠️ *SERVICE UNAVAILABLE*\n\n"
            "API configuration पूरी होने तक Number service उपलब्ध नहीं है।\n\n"
            "कोई fake/random number नहीं बनाया जाएगा।",

        "profile":
            "👤 *YOUR PROFILE*\n\n"
            "🆔 User ID: `{user_id}`\n"
            "💰 Balance: ${balance:.2f}\n"
            "👥 Total Referrals: {referrals}\n"
            "🎁 Referral Earnings: ${earnings:.2f}",

        "refer":
            "🎁 *REFERRAL PROGRAM*\n\n"
            "👥 Total Referrals: {referrals}\n"
            "💰 Referral Earnings: ${earnings:.2f}\n\n"
            "🔗 *Your Referral Link:*\n"
            "{link}",

        "withdraw":
            "💰 *WITHDRAW*\n\n"
            "💵 Current Balance: ${balance:.2f}\n\n"
            "Withdrawal system अभी तैयार किया जा रहा है।",

        "twofa":
            "🔐 *2FA CODE*\n\n"
            "अपने account की 2FA security के बारे में सुरक्षित जानकारी यहाँ देखें।\n\n"
            "⚠️ Password, OTP, 2FA secret या verification code यहाँ न भेजें।",

        "clear":
            "🗑️ Bot-side history successfully cleared.",

        "language":
            "🌐 अपनी Language चुनें:",

        "language_changed":
            "✅ Language changed successfully.",

        "closed":
            "Menu closed."
    }
}


def tr(user_id, key, **kwargs):
    lang = get_user(user_id).get("language", "bn")
    text = TEXT.get(lang, TEXT["bn"]).get(key, key)

    try:
        return text.format(**kwargs)
    except Exception:
        return text


# =========================================================
# MAIN REPLY KEYBOARD
# =========================================================

def main_keyboard():
    return ReplyKeyboardMarkup(
        [
            ["📱 GET NUMBER", "🔐 2FA CODE"],
            ["👤 PROFILE", "🎁 REFER"],
            ["💰 WITHDRAW"],
        ],
        resize_keyboard=True,
        is_persistent=True,
    )


# =========================================================
# START GATE
# =========================================================

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


# =========================================================
# MENU
# =========================================================

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


# =========================================================
# LANGUAGE
# =========================================================

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
                )
            ],
        ]
    )


# =========================================================
# SERVICES
# =========================================================

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


# =========================================================
# COUNTRIES
# =========================================================

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
    user_data = get_user(user_id)

    # Referral
    if context.args:

        try:
            referrer_id = int(context.args[0])

            if (
                referrer_id != user_id
                and user_data.get("referred_by") is None
            ):

                referrer = get_user(referrer_id)

                user_data["referred_by"] = referrer_id
                referrer["referrals"] += 1

                logger.info(
                    f"Referral added: {referrer_id} -> {user_id}"
                )

        except (ValueError, TypeError):
            pass

    logger.info(
        f"/start received from {user_id}"
    )

    await update.message.reply_text(
        "👑 *WELCOME TO AUREX NOO'R* 👑\n\n"
        "✨ *PRO VERSION*\n\n"
        "🚀 আপনার জন্য Premium Bot Experience প্রস্তুত।\n\n"
        "👇 Continue করতে নিচের button চাপুন।",
        reply_markup=start_gate_keyboard(),
        parse_mode="Markdown",
    )


# =========================================================
# MENU COMMAND
# =========================================================

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message:
        return

    user_id = update.effective_user.id

    await update.message.reply_text(
        tr(user_id, "menu"),
        reply_markup=menu_keyboard(),
        parse_mode="Markdown",
    )


# =========================================================
# HELP COMMAND
# =========================================================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message:
        return

    user_id = update.effective_user.id

    await update.message.reply_text(
        tr(user_id, "help"),
        parse_mode="Markdown",
    )


# =========================================================
# GET NUMBER
# =========================================================

async def get_number(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    await update.message.reply_text(
        tr(user_id, "get_number"),
        reply_markup=services_keyboard(),
        parse_mode="Markdown",
    )


# =========================================================
# PROFILE
# =========================================================

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    data = get_user(user_id)

    await update.message.reply_text(
        tr(
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

async def refer(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    data = get_user(user_id)

    bot_username = context.bot.username or "AurexNoorBot"

    referral_link = (
        f"https://t.me/{bot_username}?start={user_id}"
    )

    await update.message.reply_text(
        tr(
            user_id,
            "refer",
            referrals=data["referrals"],
            earnings=data["referral_earnings"],
            link=referral_link,
        ),
        parse_mode="Markdown",
    )


# =========================================================
# WITHDRAW
# =========================================================

async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    data = get_user(user_id)

    await update.message.reply_text(
        tr(
            user_id,
            "withdraw",
            balance=data["balance"],
        ),
        parse_mode="Markdown",
    )


# =========================================================
# 2FA
# =========================================================

async def twofa(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    await update.message.reply_text(
        tr(user_id, "twofa"),
        parse_mode="Markdown",
    )


# =========================================================
# TEXT HANDLER
# =========================================================

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message:
        return

    text = update.message.text

    if text == "📱 GET NUMBER":
        await get_number(update, context)

    elif text == "🔐 2FA CODE":
        await twofa(update, context)

    elif text == "👤 PROFILE":
        await profile(update, context)

    elif text == "🎁 REFER":
        await refer(update, context)

    elif text == "💰 WITHDRAW":
        await withdraw(update, context)

    else:

        user_id = update.effective_user.id

        await update.message.reply_text(
            tr(user_id, "welcome"),
            reply_markup=main_keyboard(),
            parse_mode="Markdown",
        )


# =========================================================
# CALLBACK HANDLER
# =========================================================

async def callback_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    if not query:
        return

    await query.answer()

    user_id = query.from_user.id
    data = get_user(user_id)

    callback = query.data

    # OPEN BOT
    if callback == "open_bot":

        await query.edit_message_text(
            tr(user_id, "welcome"),
            parse_mode="Markdown",
        )

        await query.message.reply_text(
            "👇 *AUREX NOO'R MAIN MENU*",
            reply_markup=main_keyboard(),
            parse_mode="Markdown",
        )

        return

    # CLEAR HISTORY
    if callback == "clear_history":

        data["history"] = []

        await query.edit_message_text(
            tr(user_id, "clear")
        )

        return

    # LANGUAGE
    if callback == "language":

        await query.edit_message_text(
            tr(user_id, "language"),
            reply_markup=language_keyboard(),
        )

        return

    # LANGUAGE CHANGE
    if callback.startswith("lang_"):

        lang = callback.replace("lang_", "")

        if lang in ("bn", "en", "hi"):
            data["language"] = lang

        await query.edit_message_text(
            tr(user_id, "language_changed")
        )

        return

    # HELP
    if callback == "help":

        await query.edit_message_text(
            tr(user_id, "help"),
            parse_mode="Markdown",
        )

        return

    # CLOSE
    if callback == "close":

        await query.edit_message_text(
            tr(user_id, "closed")
        )

        return

    # BACK MENU
    if callback == "back_menu":

        await query.edit_message_text(
            tr(user_id, "menu"),
            reply_markup=menu_keyboard(),
            parse_mode="Markdown",
        )

        return

    # SERVICE
    if callback.startswith("service_"):

        service = callback.replace("service_", "")

        data["history"].append(
            {
                "type": "service",
                "service": service,
            }
        )

        await query.edit_message_text(
            tr(user_id, "select_country"),
            reply_markup=countries_keyboard(),
            parse_mode="Markdown",
        )

        return

    # COUNTRY
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
                tr(user_id, "api_unavailable"),
                parse_mode="Markdown",
            )

            return

        await query.edit_message_text(
            "✅ API configured.\n\n"
            "Number service integration is ready for the next safe step.",
            parse_mode="Markdown",
        )

        return


# =========================================================
# ERROR HANDLER
# =========================================================

async def error_handler(update, context):

    logger.exception(
        "Unhandled exception:",
        exc_info=context.error
    )


# =========================================================
# TELEGRAM COMMANDS
# =========================================================

async def post_init(application):

    await application.bot.set_my_commands(
        [
            BotCommand(
                "start",
                "🚀 Start Bot"
            ),
            BotCommand(
                "menu",
                "⚙️ Menu"
            ),
            BotCommand(
                "help",
                "ℹ️ Help"
            ),
        ]
    )

    logger.info(
        "Telegram commands registered successfully."
    )


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
            "10000"
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

    logger.info(
        "========================================"
    )

    logger.info(
        "Aurex Noo'R PRO Version is starting..."
    )

    logger.info(
        "========================================"
    )

    if not BOT_TOKEN:

        logger.error(
            "BOT_TOKEN environment variable is missing!"
        )

        return

    # Render server
    health_thread = threading.Thread(
        target=run_health_check,
        daemon=True
    )

    health_thread.start()

    # Telegram Application
    application = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    # Commands
    application.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    application.add_handler(
        CommandHandler(
            "menu",
            menu_command
        )
    )

    application.add_handler(
        CommandHandler(
            "help",
            help_command
        )
    )

    # Inline buttons
    application.add_handler(
        CallbackQueryHandler(
            callback_handler
        )
    )

    # Reply keyboard
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            message_handler
        )
    )

    application.add_error_handler(
        error_handler
    )

    logger.info(
        "Aurex Noo'R is now polling Telegram..."
    )

    application.run_polling(
        drop_pending_updates=True
    )


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":
    main()
