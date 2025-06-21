import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from deep_translator import GoogleTranslator

API_TOKEN = "7898327343:AAHfKAfWghG7c8Kn8DDSz3ouWdbblLx7_QY"

bot = telebot.TeleBot(API_TOKEN)
user_data = {}

# زبان‌های قابل انتخاب با کدهای استاندارد
LANGUAGE_OPTIONS = {
    'فارسی (Iranian Persian)': 'fa',
    'العربية (Arabic)': 'ar',
    'English (English)': 'en',
    'Español (Spanish - Spain & Latin America)': 'es',
    'Français (French)': 'fr',
    'Deutsch (German)': 'de',
    'Italiano (Italian)': 'it',
    'Português (Portuguese - Portugal & Brazil)': 'pt',
    'Русский (Russian)': 'ru',
    'Türkçe (Turkish)': 'tr',
    '日本語 (Japanese)': 'ja',
    '한국어 (Korean)': 'ko',
    '中文 (Chinese - Mandarin)': 'zh-cn',
    'Hindi (Hindi - India)': 'hi',
    'اردو (Urdu - Pakistan & India)': 'ur',
}

def get_language_keyboard(options):
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for lang in options:
        markup.add(KeyboardButton(lang))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    user_data[message.chat.id] = {}
    markup = get_language_keyboard(['فارسی', 'العربية', 'English'])
    bot.send_message(
        message.chat.id,
        "🌐 لطفاً زبان رابط کاربری را انتخاب کن:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: m.chat.id in user_data and 'ui_lang' not in user_data[m.chat.id])
def set_ui_lang(message):
    text = message.text.strip()
    if text not in LANGUAGE_OPTIONS:
        bot.send_message(message.chat.id, "❌ لطفاً یکی از گزینه‌ها را انتخاب کن.")
        return
    user_data[message.chat.id]['ui_lang'] = text
    markup = get_language_keyboard(list(LANGUAGE_OPTIONS.keys()))
    bot.send_message(
        message.chat.id,
        "🌟 زبان مبدا (متن اصلی) را انتخاب کن:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: m.chat.id in user_data and 'src_lang' not in user_data[m.chat.id])
def set_src_lang(message):
    text = message.text.strip()
    if text not in LANGUAGE_OPTIONS:
        bot.send_message(message.chat.id, "❌ لطفاً یکی از گزینه‌ها را انتخاب کن.")
        return
    user_data[message.chat.id]['src_lang'] = LANGUAGE_OPTIONS[text]
    markup = get_language_keyboard(list(LANGUAGE_OPTIONS.keys()))
    bot.send_message(
        message.chat.id,
        "🌟 زبان مقصد (برای ترجمه) را انتخاب کن:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: m.chat.id in user_data and 'dest_lang' not in user_data[m.chat.id])
def set_dest_lang(message):
    text = message.text.strip()
    if text not in LANGUAGE_OPTIONS:
        bot.send_message(message.chat.id, "❌ لطفاً یکی از گزینه‌ها را انتخاب کن.")
        return
    user_data[message.chat.id]['dest_lang'] = LANGUAGE_OPTIONS[text]
    bot.send_message(message.chat.id, "✍️ لطفاً متنی که می‌خواهی ترجمه شود را ارسال کن:")

@bot.message_handler(func=lambda m: m.chat.id in user_data and all(k in user_data[m.chat.id] for k in ['src_lang', 'dest_lang']))
def translate_text(message):
    data = user_data[message.chat.id]
    try:
        translated = GoogleTranslator(source=data['src_lang'], target=data['dest_lang']).translate(message.text)
        bot.send_message(message.chat.id, f"🔹 ترجمه:\n{translated}")
        bot.send_message(message.chat.id, "🎉✅ ترجمه انجام شد! خوش بگردید و لذت ببرید! 🚀✨")
        user_data.pop(message.chat.id)
    except Exception:
        bot.send_message(message.chat.id, "⚠️ خطایی رخ داد، لطفاً دوباره تلاش کن.")

bot.infinity_polling()
