import asyncio
import logging
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import requests
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
# AUREX NOO'R TELEGRAM BOT — PRO (5SIM INTEGRATED)
# =========================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
FIVESIM_API_KEY = os.getenv("FIVESIM_API_KEY")

TIKTOK_URL = "https://www.tiktok.com/@aurex_noor1"
YOUTUBE_URL = "https://www.youtube.com/@ToonovaCartoon1"

FIVESIM_BASE_URL = "https://5sim.net"

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger("aurex_noor")

# =========================================================
# USER STORAGE
# =========================================================

users = {}


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
# TRANSLATIONS
# =========================================================

TEXT = {
    "bn": {
        "welcome": (
            "🌟 *AUREX NOO'R BOT*\n\n"
            "স্বাগতম! নিচের মেনু থেকে একটি অপশন নির্বাচন করুন।"
        ),
        "opened": (
            "🚀 *AUREX NOO'R*\n\n"
            "Bot menu সফলভাবে চালু হয়েছে।"
        ),
        "service_unavailable": (
            "⚠️ *SERVICE UNAVAILABLE*\n\n"
            "5SIM API configure করা নেই।"
        ),
        "api_connected": (
            "🟢 *5SIM API CONNECTED*\n\n"
            "✅ Authentication সফল\n"
            "✅ Account status পাওয়া গেছে\n\n"
            "ℹ️ নিচে থেকে দেশ ও সার্ভিস সিলেক্ট করে নাম্বার নিন।"
        ),
        "invalid_key": (
            "❌ *5SIM API KEY INVALID*\n\n"
            "Render Environment Variables থেকে API key পরীক্ষা করুন।"
        ),
        "access_denied": (
            "⛔ *5SIM ACCESS DENIED*\n\n"
            "API request অনুমোদিত হয়নি।"
        ),
        "rate_limited": (
            "⏳ *RATE LIMITED*\n\n"
            "কিছুক্ষণ পরে আবার চেষ্টা করুন।"
        ),
        "timeout": (
            "⏱️ *5SIM TIMEOUT*\n\n"
            "5SIM সময়মতো response দেয়নি।"
        ),
        "network_error": (
            "🌐 *NETWORK ERROR*\n\n"
            "5SIM-এর সাথে সংযোগ করা যায়নি।"
        ),
        "unknown_error": (
            "⚠️ *5SIM ERROR*\n\n"
            "অপ্রত্যাশিত একটি সমস্যা হয়েছে।"
        ),
        "language_updated": "✅ ভাষা সফলভাবে পরিবর্তন হয়েছে।",
        "history_cleared": "🗑️ History সফলভাবে পরিষ্কার হয়েছে।",
    },

    "en": {
        "welcome": (
            "🌟 *AUREX NOO'R BOT*\n\n"
            "Welcome! Select an option below."
        ),
        "opened": (
            "🚀 *AUREX NOO'R*\n\n"
            "Bot menu opened successfully."
        ),
        "service_unavailable": (
            "⚠️ *SERVICE UNAVAILABLE*\n\n"
            "5SIM API is not configured."
        ),
        "api_connected": (
            "🟢 *5SIM API CONNECTED*\n\n"
            "✅ Authentication successful\n"
            "✅ Account status received\n\n"
            "ℹ️ Select country and service to buy a number."
        ),
        "invalid_key": (
            "❌ *5SIM API KEY INVALID*\n\n"
            "Please check the Render Environment Variables."
        ),
        "access_denied": (
            "⛔ *5SIM ACCESS DENIED*\n\n"
            "The API request was not authorized."
        ),
        "rate_limited": (
            "⏳ *RATE LIMITED*\n\n"
            "Please try again later."
        ),
        "timeout": (
            "⏱️ *5SIM TIMEOUT*\n\n"
            "5SIM did not respond in time."
        ),
        "network_error": (
            "🌐 *NETWORK ERROR*\n\n"
            "Could not connect to 5SIM."
        ),
        "unknown_error": (
            "⚠️ *5SIM ERROR*\n\n"
            "An unexpected error occurred."
        ),
        "language_updated": "✅ Language updated successfully.",
        "history_cleared": "🗑️ History cleared successfully.",
    },

    "hi": {
        "welcome": (
            "🌟 *AUREX NOO'R BOT*\n\n"
            "स्वागत है! नीचे से एक विकल्प चुनें।"
        ),
        "opened": (
            "🚀 *AUREX NOO'R*\n\n"
            "Bot menu सफलतापूर्वक खुल गया।"
        ),
        "service_unavailable": (
            "⚠️ *SERVICE UNAVAILABLE*\n\n"
            "5SIM API configure नहीं है।"
        ),
        "api_connected": (
            "🟢 *5SIM API CONNECTED*\n\n"
            "✅ Authentication सफल\n"
            "✅ Account status प्राप्त हुआ\n\n"
            "ℹ️ नीचे से country और service चुनकर number लें।"
        ),
        "invalid_key": (
            "❌ *5SIM API KEY INVALID*\n\n"
            "Render Environment Variables जांचें।"
        ),
        "access_denied": (
            "⛔ *5SIM ACCESS DENIED*\n\n"
            "API request authorized नहीं है।"
        ),
        "rate_limited": (
            "⏳ *RATE LIMITED*\n\n"
            "बाद में फिर कोशिश करें।"
        ),
        "timeout": (
            "⏱️ *5SIM TIMEOUT*\n\n"
            "5SIM ने समय पर response नहीं दिया।"
        ),
        "network_error": (
            "🌐 *NETWORK ERROR*\n\n"
            "5SIM से connect नहीं हो सका।"
        ),
        "unknown_error": (
            "⚠️ *5SIM ERROR*\n\n"
            "एक unexpected error हुआ।"
        ),
        "language_updated": "✅ भाषा सफलतापूर्वक बदल दी गई।",
        "history_cleared": "🗑️ History साफ़ कर दी गई।",
    },
}


def tr(user_id, key):
    lang = get_user(user_id).get("language", "bn")
    return TEXT.get(lang, TEXT["bn"]).get(key, key)


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
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🎵 TikTok",
                    url=TIKTOK_URL,
                ),
                InlineKeyboardButton(
                    "▶️ YouTube",
                    url=YOUTUBE_URL,
                ),
            ],
            [
                InlineKeyboardButton(
                    "🚀 OPEN BOT",
                    callback_data="open_bot",
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
                    callback_data="clear_history",
                )
            ],
            [
                InlineKeyboardButton(
                    "🌐 Language",
                    callback_data="language",
                ),
                InlineKeyboardButton(
                    "ℹ️ Help",
                    callback_data="help",
                ),
            ],
            [
                InlineKeyboardButton(
                    "✖️ Close",
                    callback_data="close",
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
                    callback_data="lang_bn",
                ),
                InlineKeyboardButton(
                    "🇬🇧 English",
                    callback_data="lang_en",
                ),
            ],
            [
                InlineKeyboardButton(
                    "🇮🇳 हिन्दी",
                    callback_data="lang_hi",
                )
            ],
            [
                InlineKeyboardButton(
                    "🔙 Back",
                    callback_data="back_menu",
                )
            ],
        ]
    )


# =========================================================
# 5SIM API CLIENT (ADVANCED)
# =========================================================

class FiveSimClient:

    def __init__(self, api_key):
        self.api_key = api_key.strip() if api_key else None

    def configured(self):
        return bool(self.api_key)

    def headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }

    def get_profile(self):
        if not self.configured():
            return {"ok": False, "error": "not_configured"}

        try:
            response = requests.get(
                f"{FIVESIM_BASE_URL}/v1/user/profile",
                headers=self.headers(),
                timeout=10,
            )
            if response.status_code == 200:
                return {"ok": True, "data": response.json()}
            if response.status_code == 401:
                return {"ok": False, "error": "invalid_api_key"}
            if response.status_code == 403:
                return {"ok": False, "error": "access_denied"}
            if response.status_code == 429:
                return {"ok": False, "error": "rate_limited"}
            return {"ok": False, "error": f"http_{response.status_code}"}
        except requests.Timeout:
            return {"ok": False, "error": "timeout"}
        except requests.RequestException:
            return {"ok": False, "error": "network_error"}
        except Exception:
            return {"ok": False, "error": "unknown_error"}

    def buy_number(self, country="usa", operator="any", product="whatsapp"):
        if not self.configured():
            return {"ok": False, "error": "not_configured"}

        try:
            url = f"{FIVESIM_BASE_URL}/v1/user/buy/activation/{country}/{operator}/{product}"
            response = requests.get(url, headers=self.headers(), timeout=15)
            
            if response.status_code == 200:
                return {"ok": True, "data": response.json()}
            else:
                return {"ok": False, "error": response.text or f"http_{response.status_code}"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def check_order(self, order_id):
        if not self.configured():
            return {"ok": False, "error": "not_configured"}

        try:
            url = f"{FIVESIM_BASE_URL}/v1/user/check/{order_id}"
            response = requests.get(url, headers=self.headers(), timeout=10)
            
            if response.status_code == 200:
                return {"ok": True, "data": response.json()}
            else:
                return {"ok": False, "error": f"http_{response.status_code}"}
        except Exception as e:
            return {"ok": False, "error": str(e)}


fivesim = FiveSimClient(FIVESIM_API_KEY)


# =========================================================
# START
# =========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_user:
        return

    user_id = update.effective_user.id
    data = get_user(user_id)

    if context.args:
        try:
            referrer_id = int(context.args[0])
            if (
                referrer_id != user_id
                and data["referred_by"] is None
                and referrer_id in users
            ):
                data["referred_by"] = referrer_id
                users[referrer_id]["referrals"] += 1
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
    if not query or not query.message:
        return

    await query.answer()
    user_id = query.from_user.id

    await query.message.reply_text(
        tr(user_id, "opened"),
        parse_mode="Markdown",
        reply_markup=main_keyboard(),
    )


# =========================================================
# MENU
# =========================================================

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_user:
        return

    await update.message.reply_text(
        "⚙️ *AUREX NOO'R MENU*",
        parse_mode="Markdown",
        reply_markup=menu_keyboard(),
    )


# =========================================================
# HELP
# =========================================================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_user:
        return

    user_id = update.effective_user.id
    lang = get_user(user_id)["language"]

    if lang == "bn":
        text = (
            "ℹ️ *AUREX NOO'R HELP*\n\n"
            "📱 GET NUMBER — 5SIM থেকে নাম্বার এবং ওটিপি চেক করুন\n"
            "🔐 2FA CODE — 2FA সেকশন\n"
            "👤 PROFILE — অ্যাকাউন্ট ইনফরমেশন\n"
            "🎁 REFER — রেফারেল লিংক\n"
            "💰 WITHDRAW — উইথড্রল সেকশন"
        )
    else:
        text = (
            "ℹ️ *AUREX NOO'R HELP*\n\n"
            "📱 GET NUMBER — Buy number & check OTP via 5SIM\n"
            "🔐 2FA CODE — 2FA section\n"
            "👤 PROFILE — Account information\n"
            "🎁 REFER — Referral info\n"
            "💰 WITHDRAW — Withdrawal section"
        )

    await update.message.reply_text(text, parse_mode="Markdown")


# =========================================================
# GET NUMBER & 5SIM ACTIONS
# =========================================================

async def get_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_user:
        return

    user_id = update.effective_user.id

    if not fivesim.configured():
        await update.message.reply_text(
            tr(user_id, "service_unavailable"),
            parse_mode="Markdown",
        )
        return

    # কিবোর্ড বা অপশন দেখানোর জন্য ইনলাইন বাটন
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🇺🇸 USA WhatsApp", callback_data="buy_usa_whatsapp")],
        [InlineKeyboardButton("🌐 Check Active Orders", callback_data="check_orders")]
    ])

    result = await asyncio.to_thread(fivesim.get_profile)
    if not result["ok"]:
        await update.message.reply_text(tr(user_id, "invalid_key"), parse_mode="Markdown")
        return

    balance = result.get("data", {}).get("balance", "N/A")

    await update.message.reply_text(
        tr(user_id, "api_connected") + f"\n\n💰 Balance: `{balance}`\n\nনিচের বাটন থেকে অপশন বেছে নিন:",
        parse_mode="Markdown",
        reply_markup=keyboard,
    )


# =========================================================
# PROFILE
# =========================================================

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_user:
        return

    user_id = update.effective_user.id
    data = get_user(user_id)

    text = (
        "👤 *AUREX NOO'R PROFILE*\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"🆔 User ID: `{user_id}`\n"
        f"💰 Balance: ${data['balance']:.2f}\n"
        f"👥 Total Referrals: {data['referrals']}\n"
        f"🎁 Referral Earnings: ${data['referral_earnings']:.2f}\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "✨ Account Status: Active"
    )

    await update.message.reply_text(text, parse_mode="Markdown")


# =========================================================
# REFER
# =========================================================

async def refer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_user:
        return

    user_id = update.effective_user.id
    bot_username = context.bot.username or "AurexNoorBot"
    link = f"https://t.me/{bot_username}?start={user_id}"
    data = get_user(user_id)

    await update.message.reply_text(
        "🎁 *REFER & EARN*\n\n"
        "আপনার referral link:\n\n"
        f"`{link}`\n\n"
        f"👥 Referrals: {data['referrals']}\n"
        f"💰 Earnings: ${data['referral_earnings']:.2f}",
        parse_mode="Markdown",
    )


# =========================================================
# WITHDRAW & 2FA
# =========================================================

async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    await update.message.reply_text(
        "💰 *WITHDRAW*\n\nWithdrawal system is currently under development.",
        parse_mode="Markdown",
    )


async def twofa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    await update.message.reply_text(
        "🔐 *2FA CODE*\n\n2FA feature is currently under development.",
        parse_mode="Markdown",
    )


# =========================================================
# MESSAGE HANDLER
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
        await update.message.reply_text(
            "❓ Unknown option.\nPlease use the buttons below.",
            reply_markup=main_keyboard(),
        )


# =========================================================
# CALLBACK HANDLER (BUY & CHECK SMS)
# =========================================================

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query:
        return

    await query.answer()
    user_id = query.from_user.id
    data = query.data

    if data == "open_bot":
        await query.message.reply_text(
            tr(user_id, "opened"),
            parse_mode="Markdown",
            reply_markup=main_keyboard(),
        )

    elif data == "buy_usa_whatsapp":
        await query.message.reply_text("⏳ Buying USA WhatsApp number from 5SIM, please wait...")
        
        # 5sim থেকে USA WhatsApp নম্বর কেনার রিকোয়েস্ট
        res = await asyncio.to_thread(fivesim.buy_number, country="usa", operator="virtual8", product="whatsapp")
        
        if res["ok"]:
            order = res["data"]
            phone = order.get("phone")
            order_id = order.get("id")
            sms_list = order.get("sms", [])
            
            msg = (
                f"✅ *NUMBER BOUGHT SUCCESSFULLY!*\n\n"
                f"📱 Number: `+{phone}`\n"
                f"🆔 Order ID: `{order_id}`\n"
                f"📌 Status: Waiting for OTP...\n\n"
                f"শর্ত: আপনার আইপি/ভিপিএন USA হতে হবে।"
            )
            
            # ইউজারকে একটিভ অর্ডারের স্ট্যাটাস চেক করার বাটন দেওয়া
            kb = InlineKeyboardMarkup([[InlineKeyboardButton("🔄 Check OTP / SMS", callback_data=f"check_order_{order_id}")]])
            await query.message.reply_text(msg, parse_mode="Markdown", reply_markup=kb)
        else:
            await query.message.reply_text(f"❌ Failed to buy number: {res['error']}")

    elif data.startswith("check_order_"):
        order_id = data.replace("check_order_", "")
        await query.message.reply_text("🔄 Checking order status from 5SIM...")
        
        res = await asyncio.to_thread(fivesim.check_order, order_id)
        if res["ok"]:
            order = res["data"]
            status = order.get("status")
            sms_list = order.get("sms", [])
            
            sms_text = ""
            if sms_list:
                for sms in sms_list:
                    sms_text += f"\n📩 Code: `{sms.get('code')}` (Text: {sms.get('text')})"
            else:
                sms_text = "\n⏳ No OTP received yet. Please wait..."

            kb = InlineKeyboardMarkup([[InlineKeyboardButton("🔄 Refresh OTP", callback_data=f"check_order_{order_id}")]])
            await query.message.reply_text(
                f"📊 *ORDER STATUS*\n\n"
                f"🆔 ID: `{order_id}`\n"
                f"📌 Status: `{status}`"
                f"{sms_text}",
                parse_mode="Markdown",
                reply_markup=kb
            )
        else:
            await query.message.reply_text("❌ Could not fetch order status.")

    elif data == "clear_history":
        get_user(user_id)["history"] = []
        await query.message.reply_text(tr(user_id, "history_cleared"))

    elif data == "language":
        await query.message.reply_text(
            "🌐 *SELECT LANGUAGE*",
            parse_mode="Markdown",
            reply_markup=language_keyboard(),
        )

    elif data in ["lang_bn", "lang_en", "lang_hi"]:
        lang = data.replace("lang_", "")
        get_user(user_id)["language"] = lang
        await query.message.reply_text(
            tr(user_id, "language_updated"),
            reply_markup=main_keyboard(),
        )

    elif data == "help":
        await help_command(update, context)

    elif data == "close":
        try:
            await query.message.delete()
        except Exception:
            pass

    elif data == "back_menu":
        await query.message.edit_text(
            "⚙️ *AUREX NOO'R MENU*",
            parse_mode="Markdown",
            reply_markup=menu_keyboard(),
        )


# =========================================================
# ERROR HANDLER
# =========================================================

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Telegram error: %s", context.error, exc_info=context.error)


# =========================================================
# RENDER HEALTH SERVER
# =========================================================

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Aurex Noo'R Bot is running.")

    def log_message(self, format, *args):
        return


def run_health_server():
    port = int(os.getenv("PORT", "10000"))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    logger.info("Health server running on port %s", port)
    server.serve_forever()


# =========================================================
# POST INIT
# =========================================================

async def post_init(application):
    await application.bot.set_my_commands(
        [
            BotCommand("start", "Start the bot"),
            BotCommand("menu", "Open menu"),
            BotCommand("help", "Help"),
        ]
    )


# =========================================================
# MAIN
# =========================================================

def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is missing from environment variables.")

    health_thread = threading.Thread(target=run_health_server, daemon=True)
    health_thread.start()

    application = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(callback_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    application.add_error_handler(error_handler)

    logger.info("AUREX NOO'R BOT STARTING...")
    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
