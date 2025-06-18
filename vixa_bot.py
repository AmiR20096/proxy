import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

API_TOKEN = os.getenv('BOT_TOKEN', '8148296983:AAGeL81w9_RhAf4AsAlywE_YiGx0nE_aksY')
bot = telebot.TeleBot(API_TOKEN)
user_data = {}

languages = {
    'fa': 'فارسی',
    'en': 'English',
    'ar': 'العربية'
}

dns_options = {
    '403': {
        'fa': 'DNS 403 (مناسب برای اینستا، واتساپ)',
        'en': 'DNS 403 (Good for Instagram, WhatsApp)',
        'ar': 'DNS 403 (جيد لإنستغرام وواتساب)',
        'dns': ('10.202.10.10', '10.202.10.11')
    },
    'shecan': {
        'fa': 'Shecan (سریع و امن)',
        'en': 'Shecan (Fast and secure)',
        'ar': 'Shecan (سريع وآمن)',
        'dns': ('178.22.122.100', '185.51.200.2')
    },
    'electro': {
        'fa': 'Electro (پایدار و عمومی)',
        'en': 'Electro (Stable & general)',
        'ar': 'Electro (عام ومستقر)',
        'dns': ('78.157.42.100', '78.157.42.101')
    }
}

def language_keyboard():
    kb = InlineKeyboardMarkup(row_width=3)
    for code, name in languages.items():
        kb.add(InlineKeyboardButton(name, callback_data=f"lang_{code}"))
    return kb

def dns_keyboard(lang_code):
    kb = InlineKeyboardMarkup(row_width=1)
    for code, option in dns_options.items():
        kb.add(InlineKeyboardButton(option[lang_code], callback_data=f"dns_{code}"))
    return kb

def send_dns_tutorial(chat_id, lang_code, dns_code):
    dns1, dns2 = dns_options[dns_code]['dns']
    texts = {
        'fa': f"""آموزش استفاده از DNS {dns_options[dns_code]['fa']}:
1. اپلیکیشن DNS Changer را نصب کنید.
2. باز کنید و مراحل را طی کنید.
3. در بخش Primary DNS وارد کنید: `{dns1}`
4. در بخش Secondary DNS وارد کنید: `{dns2}`
5. روی Start کلیک کنید.
✅ اینترنت شما اکنون بازتر خواهد بود.""",

        'en': f"""Tutorial for using {dns_options[dns_code]['en']}:
1. Install the DNS Changer app.
2. Open and follow the steps.
3. Enter Primary DNS: `{dns1}`
4. Enter Secondary DNS: `{dns2}`
5. Tap Start.
✅ Your internet is now more open.""",

        'ar': f"""شرح استخدام {dns_options[dns_code]['ar']}:
1. قم بتثبيت تطبيق DNS Changer.
2. افتحه واتبع الخطوات.
3. أدخل DNS الأساسي: `{dns1}`
4. أدخل DNS الثانوي: `{dns2}`
5. اضغط على Start.
✅ الانترنت لديك أصبح مفتوحاً أكثر."""
    }
    bot.send_message(chat_id, texts[lang_code], parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def start(message):
    user_data[message.chat.id] = {}
    bot.send_message(message.chat.id, "لطفاً زبان خود را انتخاب کنید / Please choose your language / اختر لغتك:",
                     reply_markup=language_keyboard())

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    data = call.data

    if data.startswith("lang_"):
        lang_code = data.split("_")[1]
        user_data[chat_id] = {'lang': lang_code}
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                              text={
                                  'fa': '✅ لطفاً یکی از DNSهای زیر را انتخاب کنید:',
                                  'en': '✅ Please choose one of the DNS options:',
                                  'ar': '✅ الرجاء اختيار DNS المناسب:'
                              }[lang_code],
                              reply_markup=dns_keyboard(lang_code))

    elif data.startswith("dns_"):
        dns_code = data.split("_")[1]
        lang_code = user_data.get(chat_id, {}).get('lang', 'fa')
        send_dns_tutorial(chat_id, lang_code, dns_code)

if __name__ == "__main__":
    print("✅ ربات فعال است...")
    bot.infinity_polling()
