import logging
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    BotCommand,
)
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

# =========================================================
# ENVIRONMENT VARIABLES
# =========================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
FIVESIM_API_KEY = os.getenv("FIVESIM_API_KEY")

# =========================================================
# USER DATA
# =========================================================

# Runtime user data.
# Render restart হলে এই temporary data reset হতে পারে.
user_data_store = {}


def get_user_data(user_id):
    if user_id not in user_data_store:
        user_data_store[user_id] = {
            "language": "bn",
            "history": [],
        }

    return user_data_store[user_id]


# =========================================================
# TRANSLATIONS
# =========================================================

TEXTS = {

    "bn": {

        "welcome": (
            "🕌 *আসসালামু আলাইকুম!*\n\n"
            "👑 *Aurex Noo'R-এ আপনাকে স্বাগতম!*\n\n"
            "🤝 আমাদের Bot-এ আপনাকে স্বাগতম।\n"
            "আমাদের পরিষেবাগুলো ব্যবহার করতে নিচের "
            "Menu থেকে আপনার প্রয়োজনীয় অপশন নির্বাচন করুন।\n\n"
            "🟢 *Bot Status:* Online\n"
            "🌐 *Language:* বাংলা\n\n"
            "✨ আপনার অভিজ্ঞতা সহজ, দ্রুত ও সুন্দর রাখাই আমাদের লক্ষ্য।"
        ),

        "get_number": "💬 GET NUMBER",
        "profile": "👤 PROFILE",
        "refer": "🎁 REFER",
        "withdraw": "💰 WITHDRAW",
        "menu": "⚙️ MENU",

        "select_service": (
            "👑 *SELECT SERVICE* 👑\n\n"
            "আপনার পছন্দের সার্ভিস নির্বাচন করুন:"
        ),

        "select_country": (
            "🌍 *SELECT COUNTRY*\n\n"
            "অনুগ্রহ করে দেশ নির্বাচন করুন:"
        ),

        "menu_title": (
            "⚙️ *MENU*\n\n"
            "নিচের অপশন থেকে নির্বাচন করুন:"
        ),

        "clear_history": "🗑️ Clear History",
        "language": "🌐 Language",

        "history_cleared": (
            "✅ *History Cleared!*\n\n"
            "আপনার Bot-এর সংরক্ষিত history/data মুছে ফেলা হয়েছে।"
        ),

        "history_empty": (
            "ℹ️ আপনার কোনো সংরক্ষিত history নেই।"
        ),

        "language_title": (
            "🌐 *LANGUAGE / ভাষা*\n\n"
            "আপনার পছন্দের ভাষা নির্বাচন করুন:"
        ),

        "language_changed": "✅ ভাষা সফলভাবে পরিবর্তন করা হয়েছে।",

        "profile_text": (
            "👤 *USER PROFILE*\n\n"
            "🆔 ID: `{id}`\n"
            "📛 Name: {name}\n"
            "💰 Balance: ৳0.00\n"
            "📱 Numbers: 0"
        ),

        "refer_text": (
            "🎁 *REFERRAL PROGRAM*\n\n"
            "আপনার Referral Link বন্ধুদের সাথে শেয়ার করুন।\n\n"
            "🔗 `{link}`"
        ),

        "withdraw_text": (
            "💰 *WITHDRAW*\n\n"
            "💵 Minimum withdrawal: ৳100\n"
            "💳 Current balance: ৳0.00\n\n"
            "⚠️ আপনার পর্যাপ্ত balance নেই।"
        ),

        "api_unavailable": (
            "⚠️ *SERVICE NOT AVAILABLE*\n\n"
            "💬 Service: *{service}*\n"
            "🌍 Country: *{country}*\n\n"
            "এই মুহূর্তে API service configure করা হয়নি।\n\n"
            "🔑 API key যোগ করার পর এই service চালু করা যাবে।\n\n"
            "❌ কোনো fake/random number দেখানো হবে না।"
        ),

        "back": "🔙 Back",
        "close": "❌ Close",
        "back_menu": "⚙️ Menu",

        "twofa": (
            "🔐 *2FA Information*\n\n"
            "নিজের অ্যাকাউন্টের 2FA settings ব্যবহার করুন।\n\n"
            "⚠️ কোনো password, 2FA Secret Key অথবা "
            "verification code এখানে পাঠাবেন না।"
        ),
    },

    "en": {

        "welcome": (
            "🕌 *Assalamu Alaikum!*\n\n"
            "👑 *Welcome to Aurex Noo'R!*\n\n"
            "🤝 Welcome to our bot.\n"
            "Please select an option from the menu below "
            "to use our services.\n\n"
            "🟢 *Bot Status:* Online\n"
            "🌐 *Language:* English\n\n"
            "✨ Our goal is to keep your experience simple, "
            "fast and smooth."
        ),

        "get_number": "💬 GET NUMBER",
        "profile": "👤 PROFILE",
        "refer": "🎁 REFER",
        "withdraw": "💰 WITHDRAW",
        "menu": "⚙️ MENU",

        "select_service": (
            "👑 *SELECT SERVICE* 👑\n\n"
            "Choose your preferred service:"
        ),

        "select_country": (
            "🌍 *SELECT COUNTRY*\n\n"
            "Please select a country:"
        ),

        "menu_title": (
            "⚙️ *MENU*\n\n"
            "Choose an option below:"
        ),

        "clear_history": "🗑️ Clear History",
        "language": "🌐 Language",

        "history_cleared": (
            "✅ *History Cleared!*\n\n"
            "Your stored bot history/data has been cleared."
        ),

        "history_empty": (
            "ℹ️ You don't have any stored history."
        ),

        "language_title": (
            "🌐 *LANGUAGE*\n\n"
            "Choose your preferred language:"
        ),

        "language_changed": "✅ Language changed successfully.",

        "profile_text": (
            "👤 *USER PROFILE*\n\n"
            "🆔 ID: `{id}`\n"
            "📛 Name: {name}\n"
            "💰 Balance: ৳0.00\n"
            "📱 Numbers: 0"
        ),

        "refer_text": (
            "🎁 *REFERRAL PROGRAM*\n\n"
            "Share your referral link with friends.\n\n"
            "🔗 `{link}`"
        ),

        "withdraw_text": (
            "💰 *WITHDRAW*\n\n"
            "💵 Minimum withdrawal: ৳100\n"
            "💳 Current balance: ৳0.00\n\n"
            "⚠️ Your balance is insufficient."
        ),

        "api_unavailable": (
            "⚠️ *SERVICE NOT AVAILABLE*\n\n"
            "💬 Service: *{service}*\n"
            "🌍 Country: *{country}*\n\n"
            "The API service has not been configured yet.\n\n"
            "🔑 This service can be enabled after adding "
            "the API key.\n\n"
            "❌ No fake/random number will be displayed."
        ),

        "back": "🔙 Back",
        "close": "❌ Close",
        "back_menu": "⚙️ Menu",

        "twofa": (
            "🔐 *2FA Information*\n\n"
            "Use the 2FA settings of your own account.\n\n"
            "⚠️ Never send passwords, 2FA Secret Keys or "
            "verification codes here."
        ),
    },

    "hi": {

        "welcome": (
            "🕌 *अस्सलामु अलैकुम!*\n\n"
            "👑 *Aurex Noo'R में आपका स्वागत है!*\n\n"
            "🤝 हमारे Bot में आपका स्वागत है।\n"
            "सेवाओं का उपयोग करने के लिए नीचे दिए गए "
            "Menu से विकल्प चुनें।\n\n"
            "🟢 *Bot Status:* Online\n"
            "🌐 *Language:* हिन्दी\n\n"
            "✨ हमारा उद्देश्य आपके अनुभव को आसान, तेज़ "
            "और बेहतर बनाना है।"
        ),

        "get_number": "💬 GET NUMBER",
        "profile": "👤 PROFILE",
        "refer": "🎁 REFER",
        "withdraw": "💰 WITHDRAW",
        "menu": "⚙️ MENU",

        "select_service": (
            "👑 *SELECT SERVICE* 👑\n\n"
            "अपनी पसंद की सेवा चुनें:"
        ),

        "select_country": (
            "🌍 *SELECT COUNTRY*\n\n"
            "कृपया देश चुनें:"
        ),

        "menu_title": (
            "⚙️ *MENU*\n\n"
            "नीचे दिए गए विकल्प में से चुनें:"
        ),

        "clear_history": "🗑️ Clear History",
        "language": "🌐 Language",

        "history_cleared": (
            "✅ *History Cleared!*\n\n"
            "आपकी Bot history/data साफ कर दी गई है।"
        ),

        "history_empty": (
            "ℹ️ आपकी कोई stored history नहीं है।"
        ),

        "language_title": (
            "🌐 *LANGUAGE / भाषा*\n\n"
            "अपनी पसंदीदा भाषा चुनें:"
        ),

        "language_changed": "✅ भाषा सफलतापूर्वक बदल दी गई।",

        "profile_text": (
            "👤 *USER PROFILE*\n\n"
            "🆔 ID: `{id}`\n"
            "📛 Name: {name}\n"
            "💰 Balance: ৳0.00\n"
            "📱 Numbers: 0"
        ),

        "refer_text": (
            "🎁 *REFERRAL PROGRAM*\n\n"
            "अपना Referral Link दोस्तों के साथ शेयर करें।\n\n"
            "🔗 `{link}`"
        ),

        "withdraw_text": (
            "💰 *WITHDRAW*\n\n"
            "💵 Minimum withdrawal: ৳100\n"
            "💳 Current balance: ৳0.00\n\n"
            "⚠️ आपका balance पर्याप्त नहीं है।"
        ),

        "api_unavailable": (
            "⚠️ *SERVICE NOT AVAILABLE*\n\n"
            "💬 Service: *{service}*\n"
            "🌍 Country: *{country}*\n\n"
            "API service अभी configure नहीं की गई है।\n\n"
            "🔑 API key जोड़ने के बाद यह service चालू की जा सकती है।\n\n"
            "❌ कोई fake/random number नहीं दिखाया जाएगा।"
        ),

        "back": "🔙 Back",
        "close": "❌ Close",
        "back_menu": "⚙️ Menu",

        "twofa": (
            "🔐 *2FA Information*\n\n"
            "अपने अकाउंट की 2FA settings का उपयोग करें।\n\n"
            "⚠️ Password, 2FA Secret Key या verification "
            "code यहां कभी न भेजें।"
        ),
    },
}


def t(user_id, key, **kwargs):
    data = get_user_data(user_id)
    lang = data.get("language", "bn")

    text = TEXTS.get(lang, TEXTS["bn"]).get(key, key)

    if kwargs:
        text = text.format(**kwargs)

    return text


# =========================================================
# MAIN REPLY KEYBOARD
# =========================================================

def main_keyboard(user_id):

    return ReplyKeyboardMarkup(
        [
            [
                t(user_id, "get_number"),
                t(user_id, "profile"),
            ],
            [
                t(user_id, "refer"),
                t(user_id, "withdraw"),
            ],
            [
                t(user_id, "menu"),
            ],
        ],
        resize_keyboard=True,
    )


# =========================================================
# SERVICE KEYBOARD
# =========================================================

SERVICES = {
    "facebook_clone": "📲 FB-PC-CLONE",
    "instagram": "📸 Instagram",
    "facebook_new": "📘 Fb-New ID",
    "whatsapp": "💬 WhatsApp",
}


def services_keyboard(user_id):

    keyboard = []

    for key, name in SERVICES.items():
        keyboard.append(
            [
                InlineKeyboardButton(
                    name,
                    callback_data=f"service|{key}"
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                t(user_id, "close"),
                callback_data="close"
            )
        ]
    )

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# COUNTRY KEYBOARD
# =========================================================

COUNTRIES = {
    "india": "🇮🇳 India",
    "bangladesh": "🇧🇩 Bangladesh",
    "saudiarabia": "🇸🇦 Saudi Arabia",
    "mali": "🇲🇱 Mali",
    "madagascar": "🇲🇬 Madagascar",
    "sierraleone": "🇸🇱 Sierra Leone",
}


def country_keyboard(user_id, service_key):

    keyboard = []

    for country_key, country_name in COUNTRIES.items():

        keyboard.append(
            [
                InlineKeyboardButton(
                    country_name,
                    callback_data=f"country|{service_key}|{country_key}"
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                t(user_id, "back"),
                callback_data="services"
            )
        ]
    )

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# MENU / SETTINGS
# =========================================================

def menu_keyboard(user_id):

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    t(user_id, "clear_history"),
                    callback_data="clear_history"
                )
            ],
            [
                InlineKeyboardButton(
                    t(user_id, "language"),
                    callback_data="language"
                )
            ],
            [
                InlineKeyboardButton(
                    t(user_id, "close"),
                    callback_data="close"
                )
            ],
        ]
    )


# =========================================================
# LANGUAGE KEYBOARD
# =========================================================

def language_keyboard():

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🇧🇩 বাংলা",
                    callback_data="lang|bn"
                )
            ],
            [
                InlineKeyboardButton(
                    "🇬🇧 English",
                    callback_data="lang|en"
                )
            ],
            [
                InlineKeyboardButton(
                    "🇮🇳 हिन्दी",
                    callback_data="lang|hi"
                )
            ],
            [
                InlineKeyboardButton(
                    "🔙 Back",
                    callback_data="menu"
                )
            ],
        ]
    )


# =========================================================
# /START
# =========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user
    user_id = user.id

    get_user_data(user_id)

    await update.message.reply_text(
        t(user_id, "welcome"),
        reply_markup=main_keyboard(user_id),
        parse_mode="Markdown",
    )


# =========================================================
# /MENU
# =========================================================

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    await update.message.reply_text(
        t(user_id, "menu_title"),
        reply_markup=menu_keyboard(user_id),
        parse_mode="Markdown",
    )


# =========================================================
# MESSAGE HANDLER
# =========================================================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message or not update.message.text:
        return

    user_id = update.effective_user.id
    text = update.message.text

    # GET NUMBER
    if text == t(user_id, "get_number"):

        await update.message.reply_text(
            t(user_id, "select_service"),
            reply_markup=services_keyboard(user_id),
            parse_mode="Markdown",
        )

    # PROFILE
    elif text == t(user_id, "profile"):

        user = update.effective_user
        name = user.first_name or "User"

        await update.message.reply_text(
            t(
                user_id,
                "profile_text",
                id=user.id,
                name=name,
            ),
            parse_mode="Markdown",
        )

    # REFER
    elif text == t(user_id, "refer"):

        username = context.bot.username or "Aurex_otp_bot"

        link = f"https://t.me/{username}?start={user_id}"

        await update.message.reply_text(
            t(
                user_id,
                "refer_text",
                link=link,
            ),
            parse_mode="Markdown",
        )

    # WITHDRAW
    elif text == t(user_id, "withdraw"):

        await update.message.reply_text(
            t(user_id, "withdraw_text"),
            parse_mode="Markdown",
        )

    # MENU
    elif text == t(user_id, "menu"):

        await update.message.reply_text(
            t(user_id, "menu_title"),
            reply_markup=menu_keyboard(user_id),
            parse_mode="Markdown",
        )

    # 2FA
    elif text == "🔐 2FA CODE":

        await update.message.reply_text(
            t(user_id, "twofa"),
            parse_mode="Markdown",
        )


# =========================================================
# CALLBACK HANDLER
# =========================================================

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data

    # -----------------------------------------------------
    # CLOSE
    # -----------------------------------------------------

    if data == "close":

        try:
            await query.message.delete()
        except Exception:
            await query.edit_message_text("❌ Closed.")

        return

    # -----------------------------------------------------
    # MENU
    # -----------------------------------------------------

    if data == "menu":

        await query.edit_message_text(
            t(user_id, "menu_title"),
            reply_markup=menu_keyboard(user_id),
            parse_mode="Markdown",
        )

        return

    # -----------------------------------------------------
    # CLEAR HISTORY
    # -----------------------------------------------------

    if data == "clear_history":

        user_data = get_user_data(user_id)

        # Clear user's bot-side history
        user_data["history"] = []

        # Keep selected language
        current_language = user_data.get("language", "bn")

        user_data_store[user_id] = {
            "language": current_language,
            "history": [],
        }

        await query.edit_message_text(
            t(user_id, "history_cleared"),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            t(user_id, "back_menu"),
                            callback_data="menu"
                        )
                    ]
                ]
            ),
            parse_mode="Markdown",
        )

        return

    # -----------------------------------------------------
    # LANGUAGE
    # -----------------------------------------------------

    if data == "language":

        await query.edit_message_text(
            t(user_id, "language_title"),
            reply_markup=language_keyboard(),
            parse_mode="Markdown",
        )

        return

    # -----------------------------------------------------
    # CHANGE LANGUAGE
    # -----------------------------------------------------

    if data.startswith("lang|"):

        new_language = data.split("|")[1]

        if new_language not in ("bn", "en", "hi"):
            return

        user_data = get_user_data(user_id)

        # Keep history, change language
        user_data["language"] = new_language

        await query.edit_message_text(
            t(user_id, "language_changed"),
            reply_markup=menu_keyboard(user_id),
            parse_mode="Markdown",
        )

        # Update main keyboard too
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=t(user_id, "welcome"),
                reply_markup=main_keyboard(user_id),
                parse_mode="Markdown",
            )
        except Exception as e:
            logger.error(f"Keyboard update error: {e}")

        return

    # -----------------------------------------------------
    # SERVICES
    # -----------------------------------------------------

    if data == "services":

        await query.edit_message_text(
            t(user_id, "select_service"),
            reply_markup=services_keyboard(user_id),
            parse_mode="Markdown",
        )

        return

    # -----------------------------------------------------
    # SERVICE SELECTION
    # -----------------------------------------------------

    if data.startswith("service|"):

        service_key = data.split("|")[1]

        service_name = SERVICES.get(
            service_key,
            "Unknown Service"
        )

        await query.edit_message_text(
            f"{service_name}\n\n"
            f"{t(user_id, 'select_country')}",
            reply_markup=country_keyboard(
                user_id,
                service_key
            ),
            parse_mode="Markdown",
        )

        return

    # -----------------------------------------------------
    # COUNTRY SELECTION
    # -----------------------------------------------------

    if data.startswith("country|"):

        parts = data.split("|")

        if len(parts) != 3:
            await query.edit_message_text(
                "❌ Invalid selection."
            )
            return

        service_key = parts[1]
        country_key = parts[2]

        service_name = SERVICES.get(
            service_key,
            "Unknown"
        )

        country_name = COUNTRIES.get(
            country_key,
            country_key
        )

        # -------------------------------------------------
        # NO API KEY
        # -------------------------------------------------

        if not FIVESIM_API_KEY:

            await query.edit_message_text(
                t(
                    user_id,
                    "api_unavailable",
                    service=service_name,
                    country=country_name,
                ),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                t(user_id, "back"),
                                callback_data="services"
                            )
                        ]
                    ]
                ),
                parse_mode="Markdown",
            )

            return

        # -------------------------------------------------
        # API KEY EXISTS
        # -------------------------------------------------

        await query.edit_message_text(
            "🟢 *API CONFIGURED*\n\n"
            f"💬 Service: *{service_name}*\n"
            f"🌍 Country: *{country_name}*\n\n"
            "API integration is ready.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            t(user_id, "back"),
                            callback_data="services"
                        )
                    ]
                ]
            ),
            parse_mode="Markdown",
        )

        return


# =========================================================
# ERROR HANDLER
# =========================================================

async def error_handler(update, context):

    logger.error(
        "Exception while handling update:",
        exc_info=context.error
    )


# =========================================================
# MAIN
# =========================================================

def main():

    if not BOT_TOKEN:

        logger.error(
            "BOT_TOKEN environment variable is missing!"
        )

        return

    application = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .build()
    )

    # Commands
    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("menu", menu_command)
    )

    # Callback buttons
    application.add_handler(
        CallbackQueryHandler(handle_callback)
    )

    # Text messages
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    application.add_error_handler(error_handler)

    logger.info(
        "Aurex Noo'R Bot is starting..."
    )

    application.run_polling(
        drop_pending_updates=True
    )


# =========================================================
# RENDER HEALTH CHECK
# =========================================================

def run_health_check():

    port = int(
        os.environ.get("PORT", "8080")
    )

    server = HTTPServer(
        ("0.0.0.0", port),
        HealthCheckHandler
    )

    logger.info(
        f"Health check running on port {port}"
    )

    server.serve_forever()


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


threading.Thread(
    target=run_health_check,
    daemon=True
).start()


# =========================================================
# START
# =========================================================

if __name__ == "__main__":
    main()
