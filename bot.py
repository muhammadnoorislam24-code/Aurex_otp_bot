import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")

# User memory storage
user_data = {}

TEXTS = {
    'bn': {
        'welcome': "👋 **আসসালামু আলাইকুম!**\n\n🌟 **Aurex Noo'R** Bot-এ আপনাকে স্বাগতম! 💙\nনিচের মেনু থেকে আপনার প্রয়োজনীয় অপশন নির্বাচন করুন:",
        'get_num': "🛡 **Select service**",
        'admin_panel': "🛠 **ADMIN PANEL**",
        'clear_confirm': "⚠️ **আপনি কি সত্যিই আপনার সমস্ত ডাটা ও হিস্ট্রি মুছে ফেলতে চান?**",
        'clear_success': "✅ **আপনার সমস্ত ডাটা ও হিস্ট্রি সফলভাবে মুছে ফেলা হয়েছে!**",
        'lang_select': "🌐 **ভাষা নির্বাচন করুন / Select Language:**",
        'lang_changed': "✅ **ভাষা সফলভাবে বাংলায় পরিবর্তন করা হয়েছে!**",
        'btn_get_num': "📲 Get Number",
        'btn_leaderboard': "🏆 Leader board",
        'btn_profile': "👤 PROFILE",
        'btn_support': "🛟 SUPPORT",
        'btn_refer': "🎁 Refer",
        'btn_admin': "⚙️ ADMIN PANEL ⚙️",
        'btn_history': "🗑 Clear History",
        'btn_lang': "🌐 Language"
    },
    'en': {
        'welcome': "👋 **Welcome to Aurex Noo'R Bot!**\n\nPlease select an option from the menu below:",
        'get_num': "🛡 **Select service**",
        'admin_panel': "🛠 **ADMIN PANEL**",
        'clear_confirm': "⚠️ **Are you sure you want to clear all your history and data?**",
        'clear_success': "✅ **All your history and data have been successfully cleared!**",
        'lang_select': "🌐 **Select Language:**",
        'lang_changed': "✅ **Language successfully set to English!**",
        'btn_get_num': "📲 Get Number",
        'btn_leaderboard': "🏆 Leader board",
        'btn_profile': "👤 PROFILE",
        'btn_support': "🛟 SUPPORT",
        'btn_refer': "🎁 Refer",
        'btn_admin': "⚙️ ADMIN PANEL ⚙️",
        'btn_history': "🗑 Clear History",
        'btn_lang': "🌐 Language"
    }
}

def get_lang(user_id):
    return user_data.get(user_id, {}).get('lang', 'bn')

def main_keyboard(lang):
    t = TEXTS[lang]
    keyboard = [
        [t['btn_get_num'], t['btn_leaderboard']],
        [t['btn_history'], t['btn_support']],
        [t['btn_refer'], t['btn_profile']],
        [t['btn_lang']],
        [t['btn_admin']]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def admin_keyboard():
    keyboard = [
        [InlineKeyboardButton("VERIFY 🔴[OFF]", callback_data='toggle_verify'), InlineKeyboardButton("✏️ Edit Emoji", callback_data='edit')],
        [InlineKeyboardButton("VERMSS 🔴[OFF]", callback_data='toggle_vermss'), InlineKeyboardButton("✏️ Edit Emoji", callback_data='edit')],
        [InlineKeyboardButton("WHATNOT 🔴[OFF]", callback_data='toggle_whatnot'), InlineKeyboardButton("✏️ Edit Emoji", callback_data='edit')],
        [InlineKeyboardButton("WHATSAPP 🔴[OFF]", callback_data='toggle_whatsapp'), InlineKeyboardButton("✏️ Edit Emoji", callback_data='edit')],
        [InlineKeyboardButton("❌ Close", callback_data='close_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)

def service_keyboard():
    keyboard = [
        [InlineKeyboardButton("👾 DISCORD", callback_data='srv_discord')],
        [InlineKeyboardButton("📱 AUTHENTIFY", callback_data='srv_authentify')],
        [InlineKeyboardButton("📲 ATB", callback_data='srv_atb')],
        [InlineKeyboardButton("❌ Close", callback_data='close_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    await update.message.reply_text(
        TEXTS[lang]['welcome'],
        reply_markup=main_keyboard(lang),
        parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    lang = get_lang(user_id)
    t = TEXTS[lang]

    if text in ["📲 Get Number", t['btn_get_num']]:
        await update.message.reply_text(t['get_num'], reply_markup=service_keyboard(), parse_mode='Markdown')

    elif text in ["⚙️ ADMIN PANEL ⚙️", t['btn_admin']]:
        await update.message.reply_text(t['admin_panel'], reply_markup=admin_keyboard(), parse_mode='Markdown')

    elif text in ["🗑 Clear History", t['btn_history']]:
        keyboard = [
            [InlineKeyboardButton("✅ Yes, Clear All Data", callback_data='confirm_clear')],
            [InlineKeyboardButton("❌ Cancel", callback_data='close_menu')]
        ]
        await update.message.reply_text(t['clear_confirm'], reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif text in ["🌐 Language", t['btn_lang']]:
        keyboard = [
            [InlineKeyboardButton("🇧🇩 বাংলা (Bengali)", callback_data='set_lang_bn')],
            [InlineKeyboardButton("🇺🇸 English", callback_data='set_lang_en')]
        ]
        await update.message.reply_text(t['lang_select'], reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif text in ["👤 PROFILE", t['btn_profile']]:
        await update.message.reply_text(f"👤 **User Profile**\n\nID: `{user_id}`\nName: {update.effective_user.first_name}", parse_mode='Markdown')

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if query.data == 'close_menu':
        await query.message.delete()

    elif query.data == 'confirm_clear':
        current_lang = get_lang(user_id)
        user_data[user_id] = {'lang': current_lang}  # Clears history
        await query.edit_message_text(TEXTS[current_lang]['clear_success'], parse_mode='Markdown')

    elif query.data.startswith('set_lang_'):
        new_lang = query.data.split('_')[2]
        if user_id not in user_data:
            user_data[user_id] = {}
        user_data[user_id]['lang'] = new_lang
        await query.message.delete()
        await query.message.reply_text(
            TEXTS[new_lang]['lang_changed'],
            reply_markup=main_keyboard(new_lang),
            parse_mode='Markdown'
        )

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
