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

BOT_TOKEN = os.getenv("BOT_TOKEN")

TIKTOK_URL = "https://www.tiktok.com/@aurex_noor1"
YOUTUBE_URL = "https://www.youtube.com/@ToonovaCartoon1"

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger("AUREX_NOOR")

users = {}


# =========================================================
# USER DATA
# =========================================================

def get_user(user_id: int):
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
# TRANSLATIONS
# =========================================================

TEXTS = {
    "bn": {
        "welcome": (
            "✨ *AUREX NOO'R*\n\n"
            "স্বাগতম! 🎉\n"
            "আপনার জন্য একটি premium bot experience প্রস্তুত।\n\n"
            "নিচের menu থেকে একটি option নির্বাচন করুন।"
        ),
        "menu": "⚡ *AUREX NOO'R MENU*",
        "help": (
            "ℹ️ *AUREX NOO'R HELP*\n\n"
            "📱 GET NUMBER — Available service দেখুন\n"
            "🔐 2FA CODE — নিরাপদ 2FA তথ্য\n"
            "👤 PROFILE — আপনার account তথ্য\n"
            "🎁 REFER — referral তথ্য\n"
            "💰 WITHDRAW — balance/withdraw status\n\n"
            "🗑️ Clear History — temporary bot history পরিষ্কার করে\n"
            "🌐 Language — ভাষা পরিবর্তন করুন"
        ),
        "get_number": (
            "📱 *GET NUMBER*\n\n"
            "বর্তমানে number service API configured নেই।\n\n"
            "⚠️ কোনো fake/random number তৈরি করা হবে না।\n"
            "Service চালু করতে বৈধ ও অনুমোদিত API configuration প্রয়োজন।"
        ),
        "twofa": (
            "🔐 *2FA CODE*\n\n"
            "2FA code কারও কাছ থেকে সংগ্রহ, সংরক্ষণ বা অন্যের "
            "account-এ ব্যবহারের জন্য এই bot ব্যবহার করা যাবে না।\n\n"
            "নিজের account-এর 2FA হলে সংশ্লিষ্ট service-এর official "
            "verification page ব্যবহার করুন।"
        ),
        "profile": (
            "👤 *AUREX NOO'R PROFILE*\n\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "🆔 User ID: `{user_id}`\n"
            "💰 Balance: `${balance:.2f}`\n"
            "👥 Total Referrals: `{referrals}`\n"
            "🎁 Referral Earnings: `${earnings:.2f}`\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "✨ Account Status: *Active*"
        ),
        "refer": (
            "🎁 *REFERRAL PROGRAM*\n\n"
            "👥 Total Referrals: `{referrals}`\n"
            "💰 Referral Earnings: `${earnings:.2f}`\n\n"
            "🔗 আপনার Referral Link:\n"
            "`{link}`\n\n"
            "আপনার link ব্যবহার করে বন্ধুদের invite করতে পারেন।"
        ),
        "withdraw": (
            "💰 *WITHDRAW*\n\n"
            "Current Balance: `${balance:.2f}`\n\n"
            "⚠️ Withdrawal system বর্তমানে configuration-এর উপর নির্ভরশীল।"
        ),
        "clear": "🗑️ আপনার temporary bot history পরিষ্কার করা হয়েছে।",
        "language": "🌐 *SELECT LANGUAGE*",
        "language_changed": "✅ Language successfully changed.",
        "closed": "✕ Menu closed.",
        "back": "↩️ Back",
    },

    "en": {
        "welcome": (
            "✨ *AUREX NOO'R*\n\n"
            "Welcome! 🎉\n"
            "Your premium bot experience is ready.\n\n"
            "Choose an option below."
        ),
        "menu": "⚡ *AUREX NOO'R MENU*",
        "help": (
            "ℹ️ *AUREX NOO'R HELP*\n\n"
            "📱 GET NUMBER — View available service status\n"
            "🔐 2FA CODE — Safe 2FA information\n"
            "👤 PROFILE — View your account\n"
            "🎁 REFER — Referral information\n"
            "💰 WITHDRAW — Balance/withdrawal status\n\n"
            "🗑️ Clear History — Clears temporary bot history\n"
            "🌐 Language — Change language"
        ),
        "get_number": (
            "📱 *GET NUMBER*\n\n"
            "The number service API is not configured yet.\n\n"
            "⚠️ No fake/random numbers will be generated.\n"
            "A valid authorized API configuration is required."
        ),
        "twofa": (
            "🔐 *2FA CODE*\n\n"
            "This bot cannot collect, store, forward, or use "
            "someone else's 2FA codes.\n\n"
            "For your own account, use the service's official "
            "verification page."
        ),
        "profile": (
            "👤 *AUREX NOO'R PROFILE*\n\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "🆔 User ID: `{user_id}`\n"
            "💰 Balance: `${balance:.2f}`\n"
            "👥 Total Referrals: `{referrals}`\n"
            "🎁 Referral Earnings: `${earnings:.2f}`\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "✨ Account Status: *Active*"
        ),
        "refer": (
            "🎁 *REFERRAL PROGRAM*\n\n"
            "👥 Total Referrals: `{referrals}`\n"
            "💰 Referral Earnings: `${earnings:.2f}`\n\n"
            "🔗 Your Referral Link:\n"
            "`{link}`\n\n"
            "Invite friends using your link."
        ),
        "withdraw": (
            "💰 *WITHDRAW*\n\n"
            "Current Balance: `${balance:.2f}`\n\n"
            "⚠️ Withdrawal availability depends on configuration."
        ),
        "clear": "🗑️ Your temporary bot history has been cleared.",
        "language": "🌐 *SELECT LANGUAGE*",
        "language_changed": "✅ Language successfully changed.",
        "closed": "✕ Menu closed.",
        "back": "↩️ Back",
    },

    "hi": {
        "welcome": (
            "✨ *AUREX NOO'R*\n\n"
            "स्वागत है! 🎉\n"
            "आपका premium bot experience तैयार है।\n\n"
            "नीचे से कोई option चुनें।"
        ),
        "menu": "⚡ *AUREX NOO'R MENU*",
        "help": (
            "ℹ️ *AUREX NOO'R HELP*\n\n"
            "📱 GET NUMBER — Service status देखें\n"
            "🔐 2FA CODE — सुरक्षित 2FA जानकारी\n"
            "👤 PROFILE — Account जानकारी\n"
            "🎁 REFER — Referral जानकारी\n"
            "💰 WITHDRAW — Balance status\n\n"
            "🗑️ Clear History — Temporary history साफ करें\n"
            "🌐 Language — भाषा बदलें"
        ),
        "get_number": (
            "📱 *GET NUMBER*\n\n"
            "Number service API अभी configured नहीं है।\n\n"
            "⚠️ कोई fake/random number generate नहीं किया जाएगा।"
        ),
        "twofa": (
            "🔐 *2FA CODE*\n\n"
            "यह bot किसी अन्य व्यक्ति का 2FA code collect, store "
            "या forward नहीं करता।\n\n"
            "अपने account के लिए official verification page का उपयोग करें।"
        ),
        "profile": (
            "👤 *AUREX NOO'R PROFILE*\n\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "🆔 User ID: `{user_id}`\n"
            "💰 Balance: `${balance:.2f}`\n"
            "👥 Total Referrals: `{referrals}`\n"
            "🎁 Referral Earnings: `${earnings:.2f}`\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "✨ Account Status: *Active*"
        ),
        "refer": (
            "🎁 *REFERRAL PROGRAM*\n\n"
            "👥 Total Referrals: `{referrals}`\n"
            "💰 Referral Earnings: `${earnings:.2f}`\n\n"
            "🔗 आपका Referral Link:\n"
            "`{link}`"
        ),
        "withdraw": (
            "💰 *WITHDRAW*\n\n"
            "Current Balance: `${balance:.2f}`\n\n"
            "⚠️ Withdrawal availability configuration पर निर्भर है।"
        ),
        "clear": "🗑️ Temporary bot history साफ कर दी गई है।",
        "language": "🌐 *SELECT LANGUAGE*",
        "language_changed": "✅ Language successfully changed.",
        "closed": "✕ Menu closed.",
        "back": "↩️ Back",
    },
}


def tr(user_id: int, key: str, **kwargs):
    data = get_user(user_id)
    lang = data.get("language", "bn")

    template = TEXTS.get(lang, TEXTS["bn"]).get(key, key)

    return template.format(**kwargs)


# =========================================================
# MAIN KEYBOARD
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

def start_gate():
    keyboard = [
        [
            InlineKeyboardButton("🎵 TikTok", url=TIKTOK_URL),
            InlineKeyboardButton("▶️ YouTube", url=YOUTUBE_URL),
        ],
        [
            InlineKeyboardButton("🚀 OPEN BOT", callback_data="open_bot")
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


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
                ),
                InlineKeyboardButton(
                    "🌐 Language",
                    callback_data="language"
                ),
            ],
            [
                InlineKeyboardButton(
                    "ℹ️ Help",
                    callback_data="help"
                ),
                InlineKeyboardButton(
                    "✕ Close",
                    callback_data="close"
                ),
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
                InlineKeyboardButton("🇧🇩 বাংলা", callback_data="lang_bn"),
                InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
            ],
            [
                InlineKeyboardButton("🇮🇳 हिन्दी", callback_data="lang_hi"),
            ],
            [
                InlineKeyboardButton("↩️ Back", callback_data="menu_back")
            ],
        ]
    )


# =========================================================
# START
# =========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.message:
        return

    user_id = update.effective_user.id
    get_user(user_id)

    # Referral support
    if context.args:
        try:
            referrer_id = int(context.args[0])

            if referrer_id != user_id:
                user = get_user(user_id)

                if user.get("referred_by") is None:
                    user["referred_by"] = referrer_id

                    referrer = get_user(referrer_id)
                    referrer["referrals"] += 1

        except (ValueError, TypeError):
            pass

    await update.message.reply_text(
        tr(user_id, "welcome"),
        parse_mode="Markdown",
        reply_markup=start_gate(),
    )


# =========================================================
# OPEN BOT
# =========================================================

async def open_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if not query:
        return

    await query.answer()

    user_id = query.from_user.id

    await query.message.reply_text(
        tr(user_id, "welcome"),
        parse_mode="Markdown",
        reply_markup=main_keyboard(),
    )


# =========================================================
# MENU COMMAND
# =========================================================

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.message:
        return

    user_id = update.effective_user.id

    await update.message.reply_text(
        tr(user_id, "menu"),
        parse_mode="Markdown",
        reply_markup=menu_keyboard(),
    )


# =========================================================
# HELP
# =========================================================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.message:
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
    if not update.effective_user or not update.message:
        return

    user_id = update.effective_user.id

    await update.message.reply_text(
        tr(user_id, "get_number"),
        parse_mode="Markdown",
    )


# =========================================================
# 2FA
# =========================================================

async def twofa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.message:
        return

    user_id = update.effective_user.id

    await update.message.reply_text(
        tr(user_id, "twofa"),
        parse_mode="Markdown",
    )


# =========================================================
# PROFILE
# =========================================================

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.message:
        return

    user_id = update.effective_user.id
    data = get_user(user_id)

    text = tr(
        user_id,
        "profile",
        user_id=user_id,
        balance=float(data.get("balance", 0)),
        referrals=int(data.get("referrals", 0)),
        earnings=float(data.get("referral_earnings", 0)),
    )

    await update.message.reply_text(
        text,
        parse_mode="Markdown",
    )

    logger.info("Profile sent successfully: %s", user_id)


# =========================================================
# REFER
# =========================================================

async def refer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.message:
        return

    user_id = update.effective_user.id
    data = get_user(user_id)

    bot_username = context.bot.username

    if bot_username:
        link = f"https://t.me/{bot_username}?start={user_id}"
    else:
        link = "Bot username unavailable"

    text = tr(
        user_id,
        "refer",
        referrals=int(data.get("referrals", 0)),
        earnings=float(data.get("referral_earnings", 0)),
        link=link,
    )

    await update.message.reply_text(
        text,
        parse_mode="Markdown",
    )


# =========================================================
# WITHDRAW
# =========================================================

async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.message:
        return

    user_id = update.effective_user.id
    data = get_user(user_id)

    text = tr(
        user_id,
        "withdraw",
        balance=float(data.get("balance", 0)),
    )

    await update.message.reply_text(
        text,
        parse_mode="Markdown",
    )


# =========================================================
# MESSAGE HANDLER
# =========================================================

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_user:
        return

    text = (update.message.text or "").strip()
    user_id = update.effective_user.id

    # Store temporary history
    data = get_user(user_id)
    data["history"].append(text)

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
        await update.message.reply_text(
            tr(user_id, "menu"),
            parse_mode="Markdown",
            reply_markup=menu_keyboard(),
        )


# =========================================================
# CALLBACK HANDLER
# =========================================================

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if not query:
        return

    await query.answer()

    user_id = query.from_user.id
    data = get_user(user_id)
    action = query.data

    if action == "open_bot":
        await query.message.reply_text(
            tr(user_id, "welcome"),
            parse_mode="Markdown",
            reply_markup=main_keyboard(),
        )

    elif action == "clear_history":
        data["history"] = []

        await query.message.reply_text(
            tr(user_id, "clear")
        )

    elif action == "language":
        await query.message.reply_text(
            tr(user_id, "language"),
            parse_mode="Markdown",
            reply_markup=language_keyboard(),
        )

    elif action == "help":
        await query.message.reply_text(
            tr(user_id, "help"),
            parse_mode="Markdown",
        )

    elif action == "close":
        await query.message.reply_text(
            tr(user_id, "closed")
        )

    elif action == "menu_back":
        await query.message.reply_text(
            tr(user_id, "menu"),
            parse_mode="Markdown",
            reply_markup=menu_keyboard(),
        )

    elif action in ("lang_bn", "lang_en", "lang_hi"):
        lang = action.replace("lang_", "")

        data["language"] = lang

        await query.message.reply_text(
            tr(user_id, "language_changed")
        )

        await query.message.reply_text(
            tr(user_id, "welcome"),
            parse_mode="Markdown",
            reply_markup=main_keyboard(),
        )


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
    commands = [
        BotCommand("start", "Start the bot"),
        BotCommand("menu", "Open menu"),
        BotCommand("help", "Help & instructions"),
    ]

    await application.bot.set_my_commands(commands)


# =========================================================
# RENDER HEALTH CHECK
# =========================================================

class HealthHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(
            b"AUREX NOO'R is online."
        )

    def log_message(self, format, *args):
        return


def run_health_server():
    port = int(os.environ.get("PORT", 10000))

    server = HTTPServer(
        ("0.0.0.0", port),
        HealthHandler,
    )

    logger.info("Health server running on port %s", port)

    server.serve_forever()


# =========================================================
# MAIN
# =========================================================

def main():

    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN environment variable is missing."
        )

    # Render health server
    threading.Thread(
        target=run_health_server,
        daemon=True,
    ).start()

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
        CommandHandler("menu", menu_command)
    )

    application.add_handler(
        CommandHandler("help", help_command)
    )

    # Inline buttons
    application.add_handler(
        CallbackQueryHandler(callback_handler)
    )

    # Reply keyboard
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            message_handler,
        )
    )

    application.add_error_handler(
        error_handler
    )

    logger.info("===================================")
    logger.info("AUREX NOO'R PRO VERSION STARTING")
    logger.info("===================================")

    application.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
