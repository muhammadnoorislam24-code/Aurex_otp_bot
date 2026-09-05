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
# ENVIRONMENT
# =========================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
FIVESIM_API_KEY = os.getenv("FIVESIM_API_KEY")

# =========================================================
# SOCIAL LINKS
# =========================================================

TIKTOK_URL = "https://www.tiktok.com/@aurex_noor1"
YOUTUBE_URL = "https://www.youtube.com/@ToonovaCartoon1"

# =========================================================
# USER DATA
# =========================================================

user_data_store = {}


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

        "welcome": (
            "🕌 *আসসালামু আলাইকুম!*\n\n"
            "👑 *Aurex Noo'R-এ আপনাকে স্বাগতম!*\n\n"
            "🤝 আমাদের Bot-এ আপনাকে স্বাগতম।\n"
            "নিচের Menu থেকে আপনার প্রয়োজনীয় অপশন নির্বাচন করুন।\n\n"
            "🟢 *Bot Status:* Online\n"
            "🌐 *Language:* বাংলা\n\n"
            "✨ আপনার অভিজ্ঞতা সহজ, দ্রুত ও সুন্দর রাখাই আমাদের লক্ষ্য।"
        ),

        "get_number": "💬 GET NUMBER",
        "profile": "👤 PROFILE",
        "refer": "🎁 REFER",
        "withdraw": "💰 WITHDRAW",

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
        "help": "ℹ️ Help",

        "history_cleared": (
            "✅ *History Cleared!*\n\n"
            "আপনার Bot-side history/data মুছে ফেলা হয়েছে।"
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
            "💰 Balance: ৳{balance:.2f}\n"
            "👥 Total Referrals: {referrals}\n"
            "💵 Referral Earnings: ৳{earnings:.2f}"
        ),

        "refer_text": (
            "🎁 *REFERRAL PROGRAM*\n\n"
            "👥 *Your Referral Number:* `{referrals}`\n"
            "💵 *Referral Earnings:* ৳{earnings:.2f}\n\n"
            "🔗 *Your Referral Link:*\n"
            "`{link}`\n\n"
            "📢 বন্ধুদের এই Link শেয়ার করুন।"
        ),

        "referral_added": (
            "🎉 *Referral Added!*\n\n"
            "আপনার Referral Number এখন: `{referrals}`"
        ),

        "withdraw_text": (
            "💰 *WITHDRAW*\n\n"
            "💵 Minimum withdrawal: ৳100\n"
            "💳 Current balance: ৳{balance:.2f}\n\n"
            "⚠️ আপনার পর্যাপ্ত balance নেই।"
        ),

        "api_unavailable": (
            "⚠️ *SERVICE NOT AVAILABLE*\n\n"
            "💬 Service: *{service}*\n"
            "🌍 Country: *{country}*\n\n"
            "এই মুহূর্তে API service configure করা হয়নি।\n\n"
            "🔑 API key যোগ করার পর বৈধ API integration চালু করা যাবে।\n\n"
            "❌ কোনো fake/random number দেখানো হবে না।"
        ),

        "api_configured": (
            "🟢 *API CONFIGURED*\n\n"
            "💬 Service: *{service}*\n"
            "🌍 Country: *{country}*\n\n"
            "API key পাওয়া গেছে।\n"
            "বৈধ API integration এখানে যুক্ত করা যেতে পারে।"
        ),

        "back": "🔙 Back",
        "close": "❌ Close",
        "back_menu": "⚙️ Menu",

        "help_text": (
            "ℹ️ *Aurex Noo'R Help*\n\n"
            "💬 *GET NUMBER* — Service ও country নির্বাচন করুন।\n"
            "👤 *PROFILE* — আপনার profile দেখুন।\n"
            "🎁 *REFER* — Referral number ও link দেখুন।\n"
            "💰 *WITHDRAW* — Withdrawal status দেখুন।\n\n"
            "🌐 Language পরিবর্তন করতে Menu ব্যবহার করুন।\n"
            "🗑️ Bot-side history মুছতে Clear History ব্যবহার করুন।\n\n"
            "⚠️ Password, OTP, 2FA secret বা অন্যের verification code পাঠাবেন না।"
        ),
    },

    "en": {

        "welcome": (
            "🕌 *Assalamu Alaikum!*\n\n"
            "👑 *Welcome to Aurex Noo'R!*\n\n"
            "🤝 Welcome to our bot.\n"
            "Choose an option from the menu below.\n\n"
            "🟢 *Bot Status:* Online\n"
            "🌐 *Language:* English\n\n"
            "✨ Our goal is to keep your experience simple, fast and smooth."
        ),

        "get_number": "💬 GET NUMBER",
        "profile": "👤 PROFILE",
        "refer": "🎁 REFER",
        "withdraw": "💰 WITHDRAW",

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
        "help": "ℹ️ Help",

        "history_cleared": (
            "✅ *History Cleared!*\n\n"
            "Your stored bot-side history/data has been cleared."
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
            "💰 Balance: ৳{balance:.2f}\n"
            "👥 Total Referrals: {referrals}\n"
            "💵 Referral Earnings: ৳{earnings:.2f}"
        ),

        "refer_text": (
            "🎁 *REFERRAL PROGRAM*\n\n"
            "👥 *Your Referral Number:* `{referrals}`\n"
            "💵 *Referral Earnings:* ৳{earnings:.2f}\n\n"
            "🔗 *Your Referral Link:*\n"
            "`{link}`\n\n"
            "📢 Share this link with your friends."
        ),

        "referral_added": (
            "🎉 *Referral Added!*\n\n"
            "Your Referral Number is now: `{referrals}`"
        ),

        "withdraw_text": (
            "💰 *WITHDRAW*\n\n"
            "💵 Minimum withdrawal: ৳100\n"
            "💳 Current balance: ৳{balance:.2f}\n\n"
            "⚠️ Your balance is insufficient."
        ),

        "api_unavailable": (
            "⚠️ *SERVICE NOT AVAILABLE*\n\n"
            "💬 Service: *{service}*\n"
            "🌍 Country: *{country}*\n\n"
            "The API service has not been configured yet.\n\n"
            "❌ No fake/random number will be displayed."
        ),

        "api_configured": (
            "🟢 *API CONFIGURED*\n\n"
            "💬 Service: *{service}*\n"
            "🌍 Country: *{country}*\n\n"
            "API key detected.\n"
            "A valid API integration can be connected here."
        ),

        "back": "🔙 Back",
        "close": "❌ Close",
        "back_menu": "⚙️ Menu",

        "help_text": (
            "ℹ️ *Aurex Noo'R Help*\n\n"
            "💬 *GET NUMBER* — Select service and country.\n"
            "👤 *PROFILE* — View your profile.\n"
            "🎁 *REFER* — View referral number and link.\n"
            "💰 *WITHDRAW* — Check withdrawal status.\n\n"
            "🌐 Use Menu to change language.\n"
            "🗑️ Use Clear History to remove bot-side history.\n\n"
            "⚠️ Never send passwords, OTPs, 2FA secrets or another person's verification codes."
        ),
    },

    "hi": {

        "welcome": (
            "🕌 *अस्सलामु अलैकुम!*\n\n"
            "👑 *Aurex Noo'R में आपका स्वागत है!*\n\n"
            "🤝 हमारे Bot में आपका स्वागत है।\n"
            "नीचे दिए गए Menu से विकल्प चुनें।\n\n"
            "🟢 *Bot Status:* Online\n"
            "🌐 *Language:* हिन्दी"
        ),

        "get_number": "💬 GET NUMBER",
        "profile": "👤 PROFILE",
        "refer": "🎁 REFER",
        "withdraw": "💰 WITHDRAW",

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
        "help": "ℹ️ Help",

        "history_cleared": (
            "✅ *History Cleared!*\n\n"
            "आपकी Bot-side history/data साफ कर दी गई है।"
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
            "💰 Balance: ৳{balance:.2f}\n"
            "👥 Total Referrals: {referrals}\n"
            "💵 Referral Earnings: ৳{earnings:.2f}"
        ),

        "refer_text": (
            "🎁 *REFERRAL PROGRAM*\n\n"
            "👥 *Your Referral Number:* `{referrals}`\n"
            "💵 *Referral Earnings:* ৳{earnings:.2f}\n\n"
            "🔗 *Your Referral Link:*\n"
            "`{link}`"
        ),

        "referral_added": (
            "🎉 *Referral Added!*\n\n"
            "आपका Referral Number अब: `{referrals}`"
        ),

        "withdraw_text": (
            "💰 *WITHDRAW*\n\n"
            "💵 Minimum withdrawal: ৳100\n"
            "💳 Current balance: ৳{balance:.2f}\n\n"
            "⚠️ आपका balance पर्याप्त नहीं है।"
        ),

        "api_unavailable": (
            "⚠️ *SERVICE NOT AVAILABLE*\n\n"
            "💬 Service: *{service}*\n"
            "🌍 Country: *{country}*\n\n"
            "API service अभी configure नहीं की गई है।\n\n"
            "❌ कोई fake/random number नहीं दिखाया जाएगा।"
        ),

        "api_configured": (
            "🟢 *API CONFIGURED*\n\n"
            "💬 Service: *{service}*\n"
            "🌍 Country: *{country}*\n\n"
            "API key मिल गई है।"
        ),

        "back": "🔙 Back",
        "close": "❌ Close",
        "back_menu": "⚙️ Menu",

        "help_text": (
            "ℹ️ *Aurex Noo'R Help*\n\n"
            "💬 *GET NUMBER* — Service और country चुनें।\n"
            "👤 *PROFILE* — अपना profile देखें।\n"
            "🎁 *REFER* — Referral number और link देखें।\n"
            "💰 *WITHDRAW* — Withdrawal status देखें।\n\n"
            "⚠️ Password, OTP, 2FA secret या किसी अन्य व्यक्ति का verification code यहां न भेजें।"
        ),
    },
}


def t(user_id, key, **kwargs):

    data = get_user_data(user_id)

    lang = data.get("language", "bn")

    text = TEXTS.get(
        lang,
        TEXTS["bn"]
    ).get(
        key,
        key
    )

    if kwargs:
        text = text.format(**kwargs)

    return text


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
                ),
                InlineKeyboardButton(
                    "▶️ YouTube",
                    url=YOUTUBE_URL
                ),
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
# MAIN KEYBOARD
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
        ],
        resize_keyboard=True,
    )


# =========================================================
# SERVICES
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
# COUNTRIES
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
# MENU
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
                    t(user_id, "help"),
                    callback_data="help"
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
# LANGUAGE
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
# START
# =========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    user_id = user.id

    user_data = get_user_data(user_id)

    # -----------------------------------------------------
    # REFERRAL PROCESS
    # /start 123456789
    # -----------------------------------------------------

    if context.args:

        try:

            referrer_id = int(
                context.args[0]
            )

            # নিজের referral নিজে ব্যবহার করতে পারবে না
            if referrer_id != user_id:

                referrer = get_user_data(
                    referrer_id
                )

                # একই user আগে referred হলে আবার count হবে না
                if (
                    user_data.get("referred_by") is None
                    and referrer_id != user_data.get("referred_by")
                ):

                    user_data["referred_by"] = referrer_id

                    referrer["referrals"] += 1

                    logger.info(
                        f"Referral added: "
                        f"{referrer_id} -> {user_id}"
                    )

        except (ValueError, TypeError):

            pass

    # -----------------------------------------------------
    # START GATE
    # -----------------------------------------------------

    text = (
        "👑 *WELCOME TO AUREX NOO'R* 👑\n\n"
        "🚀 Bot ব্যবহার শুরু করুন।\n\n"
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
# MENU COMMAND
# =========================================================

async def menu_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id

    await update.message.reply_text(
        t(user_id, "menu_title"),
        reply_markup=menu_keyboard(user_id),
        parse_mode="Markdown",
    )


# =========================================================
# HELP COMMAND
# =========================================================

async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id

    await update.message.reply_text(
        t(user_id, "help_text"),
        parse_mode="Markdown",
    )


# =========================================================
# MESSAGE HANDLER
# =========================================================

async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message or not update.message.text:
        return

    user_id = update.effective_user.id

    text = update.message.text

    # -----------------------------------------------------
    # GET NUMBER
    # -----------------------------------------------------

    if text == t(user_id, "get_number"):

        await update.message.reply_text(
            t(user_id, "select_service"),
            reply_markup=services_keyboard(user_id),
            parse_mode="Markdown",
        )

    # -----------------------------------------------------
    # PROFILE
    # -----------------------------------------------------

    elif text == t(user_id, "profile"):

        user = update.effective_user

        name = user.first_name or "User"

        data = get_user_data(user_id)

        await update.message.reply_text(
            t(
                user_id,
                "profile_text",
                id=user.id,
                name=name,
                balance=data["balance"],
                referrals=data["referrals"],
                earnings=data["referral_earnings"],
            ),
            parse_mode="Markdown",
        )

    # -----------------------------------------------------
    # REFER
    # -----------------------------------------------------

    elif text == t(user_id, "refer"):

        username = context.bot.username

        if not username:
            username = "Aurex_otp_bot"

        data = get_user_data(user_id)

        link = (
            f"https://t.me/"
            f"{username}"
            f"?start={user_id}"
        )

        await update.message.reply_text(
            t(
                user_id,
                "refer_text",
                referrals=data["referrals"],
                earnings=data["referral_earnings"],
                link=link,
            ),
            parse_mode="Markdown",
        )

    # -----------------------------------------------------
    # WITHDRAW
    # -----------------------------------------------------

    elif text == t(user_id, "withdraw"):

        data = get_user_data(user_id)

        await update.message.reply_text(
            t(
                user_id,
                "withdraw_text",
                balance=data["balance"],
            ),
            parse_mode="Markdown",
        )


# =========================================================
# CALLBACK HANDLER
# =========================================================

async def handle_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    user_id = query.from_user.id

    data = query.data

    # -----------------------------------------------------
    # OPEN BOT
    # -----------------------------------------------------

    if data == "open_bot":

        await query.edit_message_text(
            t(user_id, "welcome"),
            parse_mode="Markdown",
        )

        try:

            await context.bot.send_message(
                chat_id=user_id,
                text="👇 নিচের Menu থেকে একটি option নির্বাচন করুন।",
                reply_markup=main_keyboard(user_id),
            )

        except Exception as e:

            logger.error(
                f"Keyboard update error: {e}"
            )

        return

    # -----------------------------------------------------
    # CLOSE
    # -----------------------------------------------------

    if data == "close":

        try:

            await query.message.delete()

        except Exception:

            await query.edit_message_text(
                "❌ Closed."
            )

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
    # HELP
    # -----------------------------------------------------

    if data == "help":

        await query.edit_message_text(
            t(user_id, "help_text"),
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
    # CLEAR HISTORY
    # -----------------------------------------------------

    if data == "clear_history":

        user_data = get_user_data(user_id)

        current_language = user_data.get(
            "language",
            "bn"
        )

        referrals = user_data.get(
            "referrals",
            0
        )

        earnings = user_data.get(
            "referral_earnings",
            0.0
        )

        balance = user_data.get(
            "balance",
            0.0
        )

        referred_by = user_data.get(
            "referred_by"
        )

        user_data_store[user_id] = {
            "language": current_language,
            "history": [],
            "referrals": referrals,
            "referral_earnings": earnings,
            "balance": balance,
            "referred_by": referred_by,
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

        if new_language not in (
            "bn",
            "en",
            "hi"
        ):
            return

        user_data = get_user_data(user_id)

        user_data["language"] = new_language

        await query.edit_message_text(
            t(
                user_id,
                "language_changed"
            ),
            reply_markup=menu_keyboard(user_id),
            parse_mode="Markdown",
        )

        try:

            await context.bot.send_message(
                chat_id=user_id,
                text=t(
                    user_id,
                    "welcome"
                ),
                reply_markup=main_keyboard(
                    user_id
                ),
                parse_mode="Markdown",
            )

        except Exception as e:

            logger.error(
                f"Keyboard update error: {e}"
            )

        return

    # -----------------------------------------------------
    # SERVICES
    # -----------------------------------------------------

    if data == "services":

        await query.edit_message_text(
            t(
                user_id,
                "select_service"
            ),
            reply_markup=services_keyboard(
                user_id
            ),
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
            t(
                user_id,
                "api_configured",
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


# =========================================================
# ERROR HANDLER
# =========================================================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):

    logger.error(
        "Exception while handling update:",
        exc_info=context.error
    )


# =========================================================
# RENDER HEALTH CHECK
# =========================================================

class HealthCheckHandler(
    BaseHTTPRequestHandler
):

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

    def log_message(
        self,
        format,
        *args
    ):

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
# BOT COMMANDS
# =========================================================

async def post_init(
    application
):

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


# =========================================================
# MAIN
# =========================================================

def main():

    if not BOT_TOKEN:

        logger.error(
            "BOT_TOKEN environment variable is missing!"
        )

        return

    # -----------------------------------------------------
    # HEALTH SERVER
    # -----------------------------------------------------

    health_thread = threading.Thread(
        target=run_health_check,
        daemon=True
    )

    health_thread.start()

    # -----------------------------------------------------
    # APPLICATION
    # -----------------------------------------------------

    application = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    # -----------------------------------------------------
    # COMMANDS
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # CALLBACK
    # -----------------------------------------------------

    application.add_handler(
        CallbackQueryHandler(
            handle_callback
        )
    )

    # -----------------------------------------------------
    # MESSAGES
    # -----------------------------------------------------

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    # -----------------------------------------------------
    # ERROR
    # -----------------------------------------------------

    application.add_error_handler(
        error_handler
    )

    # -----------------------------------------------------
    # START POLLING
    # -----------------------------------------------------

    logger.info(
        "Aurex Noo'R Bot is starting..."
    )

    application.run_polling(
        drop_pending_updates=True
    )


# =========================================================
# START
# =========================================================

if __name__ == "__main__":
    main()
