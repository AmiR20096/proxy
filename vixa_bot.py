import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from googletrans import Translator

API_TOKEN = "7898327343:AAHfKAfWghG7c8Kn8DDSz3ouWdbblLx7_QY"

bot = telebot.TeleBot(API_TOKEN)
translator = Translator()

# ذخیره اطلاعات کاربر
user_data = {}

LANGUAGES_UI = {
    'fa': 'فارسی',
    'ar': 'العربية',
    'en': 'English'
}

LANG_CODES = {
    'فارسی': 'fa',
    'العربية': 'ar',
    'English': 'en',
    # میتونی زبان‌های بیشتری هم اضافه کنی
    'انگلیسی': 'en',
    'عربی': 'ar',
    'فارسى': 'fa',
}

def get_language_keyboard(options):
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for lang in options:
        markup.add(KeyboardButton(lang))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    user_data[message.chat.id] = {}
    markup = get_language_keyboard(list(LANGUAGES_UI.values()))
    bot.send_message(message.chat.id, "🌐 لطفاً زبان رابط کاربری رو انتخاب کن:\nPlease choose your UI language:\nمن فضلك اختر لغة الواجهة:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.chat.id in user_data and 'ui_lang' not in user_data[message.chat.id])
def set_ui_lang(message):
    text = message.text.strip()
    if text not in LANG_CODES:
        bot.send_message(message.chat.id, "❌ لطفا یکی از گزینه‌ها را انتخاب کنید.")
        return
    user_data[message.chat.id]['ui_lang'] = LANG_CODES[text]
    # حالا از کاربر زبان مبدا رو می‌پرسیم
    markup = get_language_keyboard(['فارسی', 'العربية', 'English'])
    bot.send_message(message.chat.id, "🌟 زبان مبدا (زبان متن) را انتخاب کن:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.chat.id in user_data and 'src_lang' not in user_data[message.chat.id])
def set_src_lang(message):
    text = message.text.strip()
    if text not in LANG_CODES:
        bot.send_message(message.chat.id, "❌ لطفا یکی از گزینه‌ها را انتخاب کنید.")
        return
    user_data[message.chat.id]['src_lang'] = LANG_CODES[text]
    markup = get_language_keyboard(['فارسی', 'العربية', 'English'])
    bot.send_message(message.chat.id, "🌟 زبان مقصد (برای ترجمه) را انتخاب کن:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.chat.id in user_data and 'dest_lang' not in user_data[message.chat.id])
def set_dest_lang(message):
    text = message.text.strip()
    if text not in LANG_CODES:
        bot.send_message(message.chat.id, "❌ لطفا یکی از گزینه‌ها را انتخاب کنید.")
        return
    user_data[message.chat.id]['dest_lang'] = LANG_CODES[text]
    bot.send_message(message.chat.id, "✍️ لطفاً متنی که می‌خوای ترجمه بشه رو ارسال کن:")

@bot.message_handler(func=lambda message: message.chat.id in user_data and all(k in user_data[message.chat.id] for k in ['ui_lang','src_lang','dest_lang']))
def translate_text(message):
    data = user_data[message.chat.id]
    try:
        result = translator.translate(message.text, src=data['src_lang'], dest=data['dest_lang'])
        bot.send_message(message.chat.id, f"🔹 ترجمه:\n{result.text}")
        bot.send_message(message.chat.id, "🎉✅ ترجمه انجام شد! خوش بگردید و لذت ببرید! 🚀✨")
        # پاک کردن داده‌ها برای شروع دوباره
        user_data.pop(message.chat.id)
    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ خطایی رخ داد، لطفا دوباره امتحان کن.")

bot.infinity_polling()
