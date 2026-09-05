import logging
import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")

# User memory storage
user_data = {}

# Main Menu Keyboard (Video Style)
def main_keyboard():
    keyboard = [
        ["💬 GET NUMBER", "🔐 2FA CODE"],
        ["👤 PROFILE", "🎁 REFER"],
        ["💰 WITHDRAW"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Services Menu
def services_keyboard():
    keyboard = [
        [InlineKeyboardButton("📲 FB-PC-CLONE", callback_data='srv_FB-PC-CLONE')],
        [InlineKeyboardButton("📸 Instagram", callback_data='srv_Instagram')],
        [InlineKeyboardButton("📘 Fb-New ID", callback_data='srv_Fb-New ID')],
        [InlineKeyboardButton("💬 WhatsApp", callback_data='srv_WhatsApp')],
        [InlineKeyboardButton("❌ ব্যাক (Back)", callback_data='close_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)

# Country List Menu (For WhatsApp / Other Services)
def country_keyboard(service_name):
    keyboard = [
        [InlineKeyboardButton("🇲🇱 Mali", callback_data=f"cntry_{service_name}_Mali")],
        [InlineKeyboardButton("🇲🇬 Madagascar", callback_data=f"cntry_{service_name}_Madagascar")],
        [InlineKeyboardButton("🇧🇩 Bangladesh", callback_data=f"cntry_{service_name}_Bangladesh")],
        [InlineKeyboardButton("🇸🇦 Saudi Arabia", callback_data=f"cntry_{service_name}_SaudiArabia")],
        [InlineKeyboardButton("🇸🇱 Sierra Leone", callback_data=f"cntry_{service_name}_SierraLeone")],
        [InlineKeyboardButton("🔙 ব্যাক", callback_data='back_to_services')]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    welcome_text = (
        f"👑 **NUMBER PANEL**\n\n"
        f"👋 **স্বাগতম, {user_name}!**\n\n"
        f"আমাদের বট থেকে সার্ভিস পেতে\n"
        f"নিচের মেনু থেকে **GET NUMBER** এ চাপ দিন।"
    )
    await update.message.reply_text(welcome_text, reply_markup=main_keyboard(), parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if text == "💬 GET NUMBER":
        msg = "👑 **SELECT SERVICE** 👑\n\nপছন্দমতো সার্ভিস বেছে নিন:"
        await update.message.reply_text(msg, reply_markup=services_keyboard(), parse_mode='Markdown')

    elif text == "🔐 2FA CODE":
        await update.message.reply_text("🔑 **2FA Code Generator:**\n\nআপনার কোড জেনারেট করতে টু-ফ্যাক্টর কী (Secret Key) পাঠান।", parse_mode='Markdown')

    elif text == "👤 PROFILE":
        name = update.effective_user.first_name
        profile_text = (
            f"👤 **ইউজার প্রোফাইল**\n\n"
            f"🆔 আইডি: `{user_id}`\n"
            f"📛 নাম: {name}\n"
            f"💰 ব্যালেন্স: ৳0.00\n"
            f"📱 মোট কেনা নম্বর: 0 টি"
        )
        await update.message.reply_text(profile_text, parse_mode='Markdown')

    elif text == "🎁 REFER":
        refer_link = f"https://t.me/Aurex_otp_bot?start={user_id}"
        refer_text = (
            f"🎁 **রেফারেল প্রোগ্রাম**\n\n"
            f"আপনার রেফারেল লিংক ব্যবহার করে বন্ধুদের জয়েন করান এবং বোনাস জিতুন!\n\n"
            f"🔗 লিংক: `{refer_link}`"
        )
        await update.message.reply_text(refer_text, parse_mode='Markdown')

    elif text == "💰 WITHDRAW":
        await update.message.reply_text("💳 **উইথড্র অপশন:**\n\nসর্বনিম্ন উইথড্র limit ৳১০০ টাকা। আপনার পর্যাপ্ত ব্যালেন্স নেই।", parse_mode='Markdown')

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'close_menu':
        await query.message.delete()

    elif query.data == 'back_to_services':
        msg = "👑 **SELECT SERVICE** 👑\n\nপছন্দমতো সার্ভিস বেছে নিন:"
        await query.edit_message_text(msg, reply_markup=services_keyboard(), parse_mode='Markdown')

    elif query.data.startswith('srv_'):
        service_name = query.data.split('_')[1]
        msg = f"💬 **{service_name}**\n\nঅনুগ্ৰহ করে দেশ বেছে নিন:"
        await query.edit_message_text(msg, reply_markup=country_keyboard(service_name), parse_mode='Markdown')

    elif query.data.startswith('cntry_'):
        _, service, country = query.data.split('_')
        
        generated_num = f"+232{random.randint(10000000, 99999999)}"
        price = "35.00 BDT"
        operator = "Orange (Airtel)"
        
        num_card = (
            f"💬 **{service} ({country})**\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"📱 **নম্বর:** `{generated_num}`\n"
            f"🌍 **দেশ:** {country}\n"
            f"📶 **অপারেটর:** {operator}\n"
            f"💵 **মূল্য:** {price}\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"⌛ **ওটিপি (OTP) এর জন্য অপেক্ষা করা হচ্ছে... (৩ মিনিট)**"
        )
        
        action_keyboard = [
            [InlineKeyboardButton("📋 CP-নম্বর কপি", callback_data=f'copy_{generated_num}')],
            [InlineKeyboardButton("🔄 পরিবর্তন করুন", callback_data=f'srv_{service}')],
            [InlineKeyboardButton("❌ ক্যানসেল করুন", callback_data='close_menu')]
        ]
        
        await query.edit_message_text(num_card, reply_markup=InlineKeyboardMarkup(action_keyboard), parse_mode='Markdown')

    elif query.data.startswith('copy_'):
        num = query.data.split('_')[1]
        await query.answer(f"নম্বর কপি করা হয়েছে: {num}", show_alert=True)

def main():
    if not BOT_TOKEN:
        print("BOT_TOKEN Error!")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == '__main__':
    main()
