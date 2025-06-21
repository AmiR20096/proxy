import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from deep_translator import GoogleTranslator
import requests
import time
from flask import Flask
import threading

API_TOKEN = "7617108912:AAEKTluoS3PcFhHLTD6Xpp-ChfGjq6_MLug"

def delete_webhook():
    url = f"https://api.telegram.org/bot{API_TOKEN}/deleteWebhook"
    try:
        response = requests.get(url)
        print("🔧 Webhook delete response:", response.text)
    except Exception as e:
        print("⚠️ Couldn't delete webhook:", e)

# حذف وبهوک قبل از ساخت ربات
delete_webhook()
time.sleep(1)  # کمی صبر کن تا وبهوک کامل حذف شود

bot = telebot.TeleBot(API_TOKEN)

user_data = {}

MESSAGES = {
    'choose_ui_lang': {
        'fa': "🌐 لطفاً زبان رابط کاربری را انتخاب کن:",
        'ar': "🌐 الرجاء اختيار لغة واجهة المستخدم:",
        'en': "🌐 Please choose your UI language:"
    },
    'invalid_choice': {
        'fa': "❌ لطفاً یکی از گزینه‌ها را انتخاب کن.",
        'ar': "❌ يرجى اختيار أحد الخيارات.",
        'en': "❌ Please choose one of the options."
    },
    'welcome': {
        'fa': "👋 سلام! به ربات ترجمه خوش آمدی.",
        'ar': "👋 أهلاً بك في بوت الترجمة.",
        'en': "👋 Welcome to the translation bot!"
    },
    'choose_source_lang': {
        'fa': "🌟 زبان مبدا را انتخاب کن:",
        'ar': "🌟 اختر لغة المصدر:",
        'en': "🌟 Choose source language:"
    },
    'choose_target_lang': {
        'fa': "🌟 زبان مقصد را انتخاب کن:",
        'ar': "🌟 اختر اللغة الهدف:",
        'en': "🌟 Choose target language:"
    },
    'send_text': {
        'fa': "✍️ لطفاً متنی که می‌خواهی ترجمه شود را ارسال کن:",
        'ar': "✍️ الرجاء إرسال النص الذي تريد ترجمته:",
        'en': "✍️ Please send the text you want to translate:"
    },
    'translation_done': {
        'fa': "🎉✅ ترجمه انجام شد! از ربات استفاده کن و لذت ببر! 🌍",
        'ar': "🎉✅ تمت الترجمة! استمتع باستخدام البوت! 🌍",
        'en': "🎉✅ Translation done! Enjoy using the bot! 🌍"
    },
    'error_translation': {
        'fa': "⚠️ خطا در ترجمه: {}",
        'ar': "⚠️ خطأ في الترجمة: {}",
        'en': "⚠️ Translation error: {}"
    },
    'goodbye': {
        'fa': "👋 خداحافظ! به زودی دوباره بیای!",
        'ar': "👋 وداعاً! نأمل أن تعود قريباً!",
        'en': "👋 Goodbye! Hope to see you again soon!"
    }
}

LANGUAGE_OPTIONS = {
    'فارسی (Iran)': 'fa',
    'العربية (Arabic)': 'ar',
    'English (English)': 'en',
}

TRANSLATION_LANGS = {
    'فارسی': 'fa',
    'العربية': 'ar',
    'English': 'en',
    'Español': 'es',
    'Français': 'fr',
    'Deutsch': 'de',
    'Italiano': 'it',
    'Português': 'pt',
    'Русский': 'ru',
    'Türkçe': 'tr',
    '日本語': 'ja',
    '한국어': 'ko',
    '中文': 'zh-cn',
    'Hindi': 'hi',
    'اردو': 'ur',
}

def get_keyboard(options):
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for opt in options:
        markup.add(KeyboardButton(opt))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    user_data[message.chat.id] = {}
    markup = get_keyboard(LANGUAGE_OPTIONS.keys())
    bot.send_message(message.chat.id, MESSAGES['choose_ui_lang']['en'], reply_markup=markup)

@bot.message_handler(func=lambda m: m.chat.id in user_data and 'ui_lang' not in user_data[m.chat.id])
def set_ui_lang(message):
    if message.text not in LANGUAGE_OPTIONS:
        bot.send_message(message.chat.id, MESSAGES['invalid_choice']['en'])
        return
    user_data[message.chat.id]['ui_lang'] = LANGUAGE_OPTIONS[message.text]
    lang = user_data[message.chat.id]['ui_lang']
    bot.send_message(message.chat.id, MESSAGES['welcome'][lang])
    markup = get_keyboard(TRANSLATION_LANGS.keys())
    bot.send_message(message.chat.id, MESSAGES['choose_source_lang'][lang], reply_markup=markup)

@bot.message_handler(func=lambda m: m.chat.id in user_data and 'src_lang' not in user_data[m.chat.id])
def set_src_lang(message):
    if message.text not in TRANSLATION_LANGS:
        lang = user_data[message.chat.id]['ui_lang']
        bot.send_message(message.chat.id, MESSAGES['invalid_choice'][lang])
        return
    user_data[message.chat.id]['src_lang'] = TRANSLATION_LANGS[message.text]
    lang = user_data[message.chat.id]['ui_lang']
    markup = get_keyboard(TRANSLATION_LANGS.keys())
    bot.send_message(message.chat.id, MESSAGES['choose_target_lang'][lang], reply_markup=markup)

@bot.message_handler(func=lambda m: m.chat.id in user_data and 'dest_lang' not in user_data[m.chat.id])
def set_dest_lang(message):
    if message.text not in TRANSLATION_LANGS:
        lang = user_data[message.chat.id]['ui_lang']
        bot.send_message(message.chat.id, MESSAGES['invalid_choice'][lang])
        return
    user_data[message.chat.id]['dest_lang'] = TRANSLATION_LANGS[message.text]
    lang = user_data[message.chat.id]['ui_lang']
    bot.send_message(message.chat.id, MESSAGES['send_text'][lang])

@bot.message_handler(func=lambda m: m.chat.id in user_data and all(k in user_data[m.chat.id] for k in ['src_lang', 'dest_lang']))
def translate_text(message):
    data = user_data[message.chat.id]
    lang = data['ui_lang']
    try:
        translated = GoogleTranslator(source=data['src_lang'], target=data['dest_lang']).translate(message.text)
        bot.send_message(message.chat.id, f"🔹 {translated}")
        bot.send_message(message.chat.id, MESSAGES['translation_done'][lang])
        bot.send_message(message.chat.id, MESSAGES['goodbye'][lang])
        user_data.pop(message.chat.id)
    except Exception as e:
        bot.send_message(message.chat.id, MESSAGES['error_translation'][lang].format(str(e)))

# ساخت وب‌سرور ساده Flask برای جلوگیری از خوابیدن برنامه روی Render
app = Flask(__name__)

@app.route('/')
def home():
    return "I'm alive!", 200

def run_flask():
    app.run(host='0.0.0.0', port=5000)

# اجرای وب‌سرور در ترد جداگانه
threading.Thread(target=run_flask).start()

# اجرای ربات تلگرام با polling
bot.polling(none_stop=True)
