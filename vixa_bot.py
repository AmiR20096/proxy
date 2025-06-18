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

internet_types = {
    'wifi': {'fa': 'وای‌فای', 'en': 'Wi-Fi', 'ar': 'واي فاي'},
    'irancell': {'fa': 'ایرانسل', 'en': 'Irancell', 'ar': 'ايرانسل'},
    'mci': {'fa': 'همراه اول', 'en': 'MCI', 'ar': 'همراه اول'},
    'raitel': {'fa': 'رایتل', 'en': 'RighTel', 'ar': 'رايتل'}
}

# دی‌ان‌اس‌های جدید مخصوص اینستاگرام و سایت‌های مهم
proxies = {
    'wifi': [
        ("1.1.1.1", "1.0.0.1"),
        ("8.8.8.8", "8.8.4.4"),
        ("94.140.14.14", "94.140.15.15"),
        ("185.228.168.168", "185.228.169.168"),
        ("208.67.222.222", "208.67.220.220")
    ],
    'irancell': [
        ("1.1.1.1", "1.0.0.1"),
        ("8.8.8.8", "8.8.4.4"),
        ("94.140.14.14", "94.140.15.15"),
        ("185.228.168.168", "185.228.169.168"),
        ("208.67.222.222", "208.67.220.220")
    ],
    'mci': [
        ("1.1.1.1", "1.0.0.1"),
        ("8.8.8.8", "8.8.4.4"),
        ("94.140.14.14", "94.140.15.15"),
        ("185.228.168.168", "185.228.169.168"),
        ("208.67.222.222", "208.67.220.220")
    ],
    'raitel': [
        ("1.1.1.1", "1.0.0.1"),
        ("8.8.8.8", "8.8.4.4"),
        ("94.140.14.14", "94.140.15.15"),
        ("185.228.168.168", "185.228.169.168"),
        ("208.67.222.222", "208.67.220.220")
    ]
}

def language_keyboard():
    kb = InlineKeyboardMarkup(row_width=3)
    for code, name in languages.items():
        kb.add(InlineKeyboardButton(name, callback_data=f"lang_{code}"))
    return kb

def internet_keyboard(lang_code):
    kb = InlineKeyboardMarkup(row_width=2)
    for code, names in internet_types.items():
        kb.add(InlineKeyboardButton(names[lang_code], callback_data=f"internet_{code}"))
    return kb

def send_proxies(chat_id, internet_code, lang_code):
    proxy_list = proxies.get(internet_code, [])
    texts = {
        'fa': "🧩 پروکسی‌های مناسب:\n\n",
        'en': "🧩 Suitable DNS addresses:\n\n",
        'ar': "🧩 DNS المناسب:\n\n"
    }
    text = texts[lang_code]
    for i, (primary, secondary) in enumerate(proxy_list, 1):
        text += f"{i}. 🟢 Primary: `{primary}`\n   🔵 Secondary: `{secondary}`\n\n"
    bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup().add(
        InlineKeyboardButton({'fa': 'آموزش', 'en': 'Tutorial', 'ar': 'تعليم'}[lang_code], callback_data="show_tutorial")
    ))

def send_tutorial(chat_id, lang_code, internet_code):
    texts = {
        'fa': f"""🎓 آموزش استفاده از DNS برای {internet_types[internet_code]['fa']}:

1. برنامه DNS Changer را نصب کنید (از گوگل‌پلی یا بازار).
2. برنامه را باز کنید.
3. بخش Primary DNS را با مقدار اول پر کنید.
4. بخش Secondary DNS را با مقدار دوم پر کنید.
5. دکمه START را بزنید.
6. برای قطع، STOP را بزنید.""",
        'en': f"""🎓 Tutorial for {internet_types[internet_code]['en']}:

1. Install DNS Changer from Google Play or App Store.
2. Open the app.
3. Enter the Primary DNS as the first address.
4. Enter the Secondary DNS as the second address.
5. Tap START.
6. Tap STOP to disconnect.""",
        'ar': f"""🎓 تعليم استخدام DNS لـ {internet_types[internet_code]['ar']}:

1. ثبت DNS Changer من Google Play أو App Store.
2. افتح التطبيق.
3. أدخل Primary DNS بالبروكسي الأول.
4. أدخل Secondary DNS بالبروكسي الثاني.
5. اضغط START للاتصال.
6. اضغط STOP لقطع الاتصال."""
    }
    bot.send_message(chat_id, texts[lang_code])

@bot.message_handler(commands=['start'])
def start(message):
    user_data[message.chat.id] = {}
    bot.send_message(message.chat.id, "لطفاً زبان خود را انتخاب کنید / Please choose your language / اختر لغتك:",
                     reply_markup=language_keyboard())

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    data = call.data

    if data.startswith("lang_"):
        lang_code = data.split("_")[1]
        user_data[chat_id]['lang'] = lang_code
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                              text={
                                  'fa': 'لطفاً نوع اینترنت خود را انتخاب کنید:',
                                  'en': 'Please choose your internet type:',
                                  'ar': 'يرجى اختيار نوع الانترنت:'
                              }[lang_code],
                              reply_markup=internet_keyboard(lang_code))

    elif data.startswith("internet_"):
        internet_code = data.split("_")[1]
        user_data[chat_id]['internet'] = internet_code
        lang_code = user_data[chat_id].get('lang', 'fa')
        send_proxies(chat_id, internet_code, lang_code)

    elif data == "show_tutorial":
        lang_code = user_data[chat_id].get('lang', 'fa')
        internet_code = user_data[chat_id].get('internet', 'wifi')
        send_tutorial(chat_id, lang_code, internet_code)

# اجرای ربات
if __name__ == "__main__":
    print("✅ ربات با موفقیت در Render اجرا شد...")
    bot.remove_webhook()  # رفع خطای 409
    bot.infinity_polling()
