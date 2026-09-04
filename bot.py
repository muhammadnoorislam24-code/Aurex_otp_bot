import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Telegram Bot Token
BOT_TOKEN = "8831932429:AAEkqVliTDfIag-sGYKMp0BuJSlbeBBi2bY"

user_data = {}
orders = {}

TEXTS = {
    'bn': {
        'welcome': (
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🌟 আসসালামু আলাইকুম! 🌟\n\n"
            "🤖 **Aurex Noo'R** Bot-এ আপনাকে স্বাগতম! 💙\n\n"
            "আপনাকে আমাদের বটে পেয়ে আমরা আনন্দিত। 😊\n"
            "এই বটটি দ্রুত ও সহজভাবে OTP Verification সংক্রান্ত সেবা ব্যবহারের জন্য তৈরি করা হয়েছে।\n\n"
            "🔐 নিরাপদ • দ্রুত • সহজ\n\n"
            "📌 নিচের মেনু থেকে আপনার প্রয়োজনীয় অপশন নির্বাচন করুন।\n\n"
            "⚡ Aurex Noo'R — Fast • Secure • Reliable\n\n"
            "❤️ ধন্যবাদ আমাদের বট ব্যবহার করার জন্য!\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        'settings_title': (
            "⚙️ **SETTINGS**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "নিচের অপশনগুলো থেকে আপনার প্রয়োজনীয় সেটিংস বেছে নিন:"
        ),
        'clear_confirm': (
            "⚠️ **Clear History**\n\n"
            "আপনি কি সত্যিই আপনার History মুছে ফেলতে চান?\n\n"
            "❗ শুধুমাত্র আপনার নিজের সংরক্ষিত History মুছে যাবে।"
        ),
        'clear_success': (
            "✅ **History Cleared Successfully!**\n\n"
            "আপনার History সফলভাবে মুছে ফেলা হয়েছে।"
        ),
        'lang_title': (
            "🌐 **LANGUAGE SETTINGS**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🌐 **Select Language / ভাষা নির্বাচন করুন:**"
        ),
        'about_text': (
            "ℹ️ **ABOUT BOT**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🤖 **Aurex Noo'R**\n\n"
            "⚡ Fast • Secure • Reliable\n\n"
            "Aurex Noo'R is a modern Telegram service bot with a simple and user-friendly interface.\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        'select_srv': (
            "SERVICE SELECTION\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🛡️ **Select Service:**"
        ),
        'select_cnt': "🌍 **Selected Service:** {srv}\n\nএখন দেশ নির্বাচন করুন:",
        'demo_allocated': (
            "ORDER STATUS UI\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "✅ **Demo Number Allocated!**\n\n"
            "📌 **Service:** {srv}\n"
            "🌍 **Country:** {cnt}\n"
            "📱 **Number:** `{num}`\n"
            "⏱️ **Status:** Waiting for SMS..."
        ),
        'otp_recv': "🎉 **OTP Received!**\n\n🔑 **Your Code:** `{otp}`",
        'cancelled': "❌ Order cancelled successfully.",
        'btn_get_num': "📱 Get Number",
        'btn_settings': "⚙️ Settings",
        'btn_clear': "🗑️ Clear History",
        'btn_lang': "🌐 Language",
        'btn_about': "ℹ️ About Bot",
        'btn_back': "⬅️ Back",
        'btn_yes_clear': "✅ Yes, Clear",
        'btn_cancel': "❌ Cancel",
        'btn_start': "🚀 Start",
        'btn_close': "❌ Close"
    },
    'en': {
        'welcome': (
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🌟 Assalamu Alaikum! 🌟\n\n"
            "🤖 Welcome to **Aurex Noo'R** Bot! 💙\n\n"
            "We are glad to have you here. 😊\n"
            "This bot is designed for fast and easy OTP Verification services.\n\n"
            "🔐 Safe • Fast • Simple\n\n"
            "📌 Please select your required option from the menu below.\n\n"
            "⚡ Aurex Noo'R — Fast • Secure • Reliable\n\n"
            "❤️ Thank you for using our bot!\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        'settings_title': (
            "⚙️ **SETTINGS**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "Choose your desired setting option below:"
        ),
        'clear_confirm': (
            "⚠️ **Clear History**\n\n"
            "Are you sure you want to delete your History?\n\n"
            "❗ Only your own stored History will be deleted."
        ),
        'clear_success': (
            "✅ **History Cleared Successfully!**\n\n"
            "Your history has been deleted successfully."
        ),
        'lang_title': (
            "🌐 **LANGUAGE SETTINGS**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🌐 **Select Language:**"
        ),
        'about_text': (
            "ℹ️ **ABOUT BOT**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🤖 **Aurex Noo'R**\n\n"
            "⚡ Fast • Secure • Reliable\n\n"
            "Aurex Noo'R is a modern Telegram service bot with a simple and user-friendly interface.\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        'select_srv': (
            "SERVICE SELECTION\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🛡️ **Select Service:**"
        ),
        'select_cnt': "🌍 **Selected Service:** {srv}\n\nNow select country:",
        'demo_allocated': (
            "ORDER STATUS UI\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "✅ **Demo Number Allocated!**\n\n"
            "📌 **Service:** {srv}\n"
            "🌍 **Country:** {cnt}\n"
            "📱 **Number:** `{num}`\n"
            "⏱️ **Status:** Waiting for SMS..."
        ),
        'otp_recv': "🎉 **OTP Received!**\n\n🔑 **Your Code:** `{otp}`",
        'cancelled': "❌ Order cancelled successfully.",
        'btn_get_num': "📱 Get Number",
        'btn_settings': "⚙️ Settings",
        'btn_clear': "🗑️ Clear History",
        'btn_lang': "🌐 Language",
        'btn_about': "ℹ️ About Bot",
        'btn_back': "⬅️ Back",
        'btn_yes_clear': "✅ Yes, Clear",
        'btn_cancel': "❌ Cancel",
        'btn_start': "🚀 Start",
        'btn_close': "❌ Close"
    },
    'hi': {
        'welcome': (
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🌟 अस्सलाम वालेकुम! 🌟\n\n"
            "🤖 **Aurex Noo'R** Bot में आपका स्वागत है! 💙\n\n"
            "हमें आपको यहां पाकर खुशी हुई। 😊\n"
            "यह बॉट तेज़ और आसान OTP सत्यापन सेवाओं के लिए डिज़ाइन किया गया है।\n\n"
            "🔐 सुरक्षित • तेज़ • आसान\n\n"
            "📌 कृपया नीचे दिए गए मेनू से अपना विकल्प चुनें।\n\n"
            "⚡ Aurex Noo'R — Fast • Secure • Reliable\n\n"
            "❤️ हमारे बॉट का उपयोग करने के लिए धन्यवाद!\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        'settings_title': (
            "⚙️ **SETTINGS**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "नीचे दिए गए विकल्पों में से अपनी सेटिंग चुनें:"
        ),
        'clear_confirm': (
            "⚠️ **Clear History**\n\n"
            "क्या आप वाकई अपना इतिहास हटाना चाहते हैं?\n\n"
            "❗ केवल आपका अपना संग्रहीत इतिहास ही हटाया जाएगा।"
        ),
        'clear_success': (
            "✅ **History Cleared Successfully!**\n\n"
            "आपका इतिहास सफलतापूर्वक हटा दिया गया है।"
        ),
        'lang_title': (
            "🌐 **LANGUAGE SETTINGS**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🌐 **Select Language / भाषा चुनें:**"
        ),
        'about_text': (
            "ℹ️ **ABOUT BOT**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🤖 **Aurex Noo'R**\n\n"
            "⚡ Fast • Secure • Reliable\n\n"
            "Aurex Noo'R is a modern Telegram service bot with a simple and user-friendly interface.\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        'select_srv': (
            "SERVICE SELECTION\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🛡️ **Select Service:**"
        ),
        'select_cnt': "🌍 **चयनित सेवा:** {srv}\n\nअब देश चुनें:",
        'demo_allocated': (
            "ORDER STATUS UI\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "✅ **Demo Number Allocated!**\n\n"
            "📌 **Service:** {srv}\n"
            "🌍 **Country:** {cnt}\n"
            "📱 **Number:** `{num}`\n"
            "⏱️ **Status:** Waiting for SMS..."
        ),
        'otp_recv': "🎉 **OTP Received!**\n\n🔑 **Your Code:** `{otp}`",
        'cancelled': "❌ ऑर्डर सफलतापूर्वक रद्द कर दिया गया।",
        'btn_get_num': "📱 Get Number",
        'btn_settings': "⚙️ Settings",
        'btn_clear': "🗑️ Clear History",
        'btn_lang': "🌐 Language",
        'btn_about': "ℹ️ About Bot",
        'btn_back': "⬅️ Back",
        'btn_yes_clear': "✅ Yes, Clear",
        'btn_cancel': "❌ Cancel",
        'btn_start': "🚀 Start",
        'btn_close': "❌ Close"
    }
}

def get_lang(user_id):
    return user_data.get(user_id, {}).get('lang', 'bn')

def get_main_keyboard(lang='bn'):
    t = TEXTS[lang]
    keyboard = [
        [InlineKeyboardButton(t['btn_get_num'], callback_data='btn_get_number')],
        [InlineKeyboardButton("🔵 Discord", callback_data='srv_discord'), InlineKeyboardButton("📱 WhatsApp", callback_data='srv_whatsapp')],
        [InlineKeyboardButton("✈️ Telegram", callback_data='srv_telegram')],
        [InlineKeyboardButton(t['btn_settings'], callback_data='btn_settings')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_settings_keyboard(lang='bn'):
    t = TEXTS[lang]
    keyboard = [
        [InlineKeyboardButton(t['btn_clear'], callback_data='btn_clear_history')],
        [InlineKeyboardButton(t['btn_lang'], callback_data='btn_language')],
        [InlineKeyboardButton(t['btn_about'], callback_data='btn_about')],
        [InlineKeyboardButton(t['btn_back'], callback_data='btn_main_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)

async def post_init(application):
    await application.bot.set_my_commands([
        BotCommand("start", "🚀 Start / Restart Bot"),
        BotCommand("settings", "⚙️ Settings"),
        BotCommand("clear", "🗑️ Clear History"),
        BotCommand("language", "🌐 Language"),
        BotCommand("about", "ℹ️ About Bot")
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id not in user_data:
        user_data[user.id] = {"lang": "bn", "history": []}
        
    lang = get_lang(user.id)
    txt = TEXTS[lang]
    
    await update.message.reply_text(
        txt['welcome'], 
        reply_markup=get_main_keyboard(lang), 
        parse_mode='Markdown'
    )

async def cmd_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update.effective_user.id)
    txt = TEXTS[lang]
    await update.message.reply_text(txt['settings_title'], reply_markup=get_settings_keyboard(lang), parse_mode='Markdown')

async def cmd_clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update.effective_user.id)
    txt = TEXTS[lang]
    keyboard = [
        [InlineKeyboardButton(txt['btn_yes_clear'], callback_data='confirm_clear_yes')],
        [InlineKeyboardButton(txt['btn_cancel'], callback_data='btn_settings')]
    ]
    await update.message.reply_text(txt['clear_confirm'], reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def cmd_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update.effective_user.id)
    txt = TEXTS[lang]
    keyboard = [
        [InlineKeyboardButton("🇧🇩 বাংলা", callback_data='setlang_bn')],
        [InlineKeyboardButton("🇬🇧 English", callback_data='setlang_en')],
        [InlineKeyboardButton("🇮🇳 हिन्दी", callback_data='setlang_hi')],
        [InlineKeyboardButton(txt['btn_back'], callback_data='btn_settings')]
    ]
    await update.message.reply_text(txt['lang_title'], reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def cmd_about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update.effective_user.id)
    txt = TEXTS[lang]
    keyboard = [[InlineKeyboardButton(txt['btn_back'], callback_data='btn_settings')]]
    await update.message.reply_text(txt['about_text'], reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    if user_id not in user_data:
        user_data[user_id] = {"lang": "bn", "history": []}

    lang = get_lang(user_id)
    txt = TEXTS[lang]

    if query.data == 'btn_main_menu':
        await query.edit_message_text(txt['welcome'], reply_markup=get_main_keyboard(lang), parse_mode='Markdown')

    elif query.data == 'btn_settings':
        await query.edit_message_text(txt['settings_title'], reply_markup=get_settings_keyboard(lang), parse_mode='Markdown')

    elif query.data == 'btn_clear_history':
        keyboard = [
            [InlineKeyboardButton(txt['btn_yes_clear'], callback_data='confirm_clear_yes')],
            [InlineKeyboardButton(txt['btn_cancel'], callback_data='btn_settings')]
        ]
        await query.edit_message_text(txt['clear_confirm'], reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif query.data == 'confirm_clear_yes':
        user_data[user_id]['history'] = []
        keyboard = [[InlineKeyboardButton(txt['btn_start'], callback_data='btn_main_menu')]]
        await query.edit_message_text(txt['clear_success'], reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif query.data == 'btn_language':
        keyboard = [
            [InlineKeyboardButton("🇧🇩 বাংলা", callback_data='setlang_bn')],
            [InlineKeyboardButton("🇬🇧 English", callback_data='setlang_en')],
            [InlineKeyboardButton("🇮🇳 हिन्दी", callback_data='setlang_hi')],
            [InlineKeyboardButton(txt['btn_back'], callback_data='btn_settings')]
        ]
        await query.edit_message_text(txt['lang_title'], reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif query.data.startswith('setlang_'):
        new_lang = query.data.split('_')[1]
        user_data[user_id]['lang'] = new_lang
        updated_txt = TEXTS[new_lang]
        await query.edit_message_text(updated_txt['welcome'], reply_markup=get_main_keyboard(new_lang), parse_mode='Markdown')

    elif query.data == 'btn_about':
        keyboard = [[InlineKeyboardButton(txt['btn_back'], callback_data='btn_settings')]]
        await query.edit_message_text(txt['about_text'], reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif query.data == 'btn_get_number':
        keyboard = [
            [InlineKeyboardButton("🔵 Discord", callback_data='srv_discord')],
            [InlineKeyboardButton("📱 WhatsApp", callback_data='srv_whatsapp')],
            [InlineKeyboardButton("✈️ Telegram", callback_data='srv_telegram')],
            [InlineKeyboardButton(txt['btn_close'], callback_data='btn_main_menu')]
        ]
        await query.edit_message_text(txt['select_srv'], reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif query.data.startswith('srv_'):
        service_name = query.data.split('_')[1].capitalize()
        keyboard = [
            [InlineKeyboardButton("🇧🇩 Bangladesh (+880)", callback_data=f'cnt_bangladesh_{service_name}')],
            [InlineKeyboardButton("🇮🇳 India (+91)", callback_data=f'cnt_india_{service_name}')],
            [InlineKeyboardButton("🇺🇸 USA (+1)", callback_data=f'cnt_usa_{service_name}')],
            [InlineKeyboardButton(txt['btn_back'], callback_data='btn_get_number')]
        ]
        await query.edit_message_text(txt['select_cnt'].format(srv=service_name), reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif query.data.startswith('cnt_'):
        _, country, service = query.data.split('_')
        prefixes = {"bangladesh": "+88017", "india": "+9198", "usa": "+1202"}
        prefix = prefixes.get(country, "+1555")
        fake_number = prefix + "".join([str(random.randint(0, 9)) for _ in range(8)])
        order_id = str(random.randint(100000, 999999))
        fake_otp = str(random.randint(100000, 999999))
        
        orders[order_id] = {"otp": fake_otp, "user_id": user_id}
        user_data[user_id]['history'].append(order_id)

        keyboard = [
            [InlineKeyboardButton("📩 Check OTP", callback_data=f'checkotp_{order_id}')],
            [InlineKeyboardButton("❌ Cancel Order", callback_data=f'cancel_{order_id}')]
        ]
        await query.edit_message_text(
            txt['demo_allocated'].format(srv=service.capitalize(), cnt=country.capitalize(), num=fake_number),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )

    elif query.data.startswith('checkotp_'):
        order_id = query.data.split('_')[1]
        order_info = orders.get(order_id)
        if order_info:
            otp_code = order_info["otp"]
            keyboard = [[InlineKeyboardButton(txt['btn_back'], callback_data='btn_main_menu')]]
            await query.edit_message_text(
                txt['otp_recv'].format(otp=otp_code),
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )

    elif query.data.startswith('cancel_'):
        order_id = query.data.split('_')[1]
        if order_id in orders:
            del orders[order_id]
        keyboard = [[InlineKeyboardButton(txt['btn_back'], callback_data='btn_main_menu')]]
        await query.edit_message_text(txt['cancelled'], reply_markup=InlineKeyboardMarkup(keyboard))

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).post_init(post_init).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("settings", cmd_settings))
    app.add_handler(CommandHandler("clear", cmd_clear))
    app.add_handler(CommandHandler("language", cmd_language))
    app.add_handler(CommandHandler("about", cmd_about))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("Aurex Noo'R Bot is running successfully...")
    app.run_polling()
  
