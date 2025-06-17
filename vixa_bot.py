import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '8148296983:AAGeL81w9_RhAf4AsAlywE_YiGx0nE_aksY'
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

proxies = {
    'wifi': [
        ("185.195.232.44:8080", "198.50.163.192:3128"),
        ("103.216.82.110:6667", "103.250.166.50:6667"),
        ("192.140.32.101:1080", "104.223.145.100:8080"),
        ("91.205.239.36:3128", "198.50.163.192:3128"),
        ("103.145.77.53:80", "178.33.136.99:3128")
    ],
    'irancell': [
        ("51.89.144.230:8080", "51.89.144.231:8080"),
        ("51.158.186.141:5836", "51.158.123.35:8811"),
        ("185.189.210.74:80", "178.62.193.19:3128"),
        ("103.216.82.140:6667", "103.216.82.137:6667"),
        ("103.48.70.198:6667", "103.48.70.199:6667")
    ],
    'mci': [
        ("103.216.82.210:6667", "103.216.82.211:6667"),
        ("103.48.70.244:6667", "103.48.70.245:6667"),
        ("45.77.141.123:3128", "45.77.141.124:3128"),
        ("103.216.82.135:6667", "103.216.82.136:6667"),
        ("45.77.142.125:3128", "45.77.142.126:3128")
    ],
    'raitel': [
        ("103.216.82.230:6667", "103.216.82.231:6667"),
        ("103.48.70.254:6667", "103.48.70.255:6667"),
        ("45.77.143.123:3128", "45.77.143.124:3128"),
        ("103.216.82.240:6667", "103.216.82.241:6667"),
        ("45.77.144.125:3128", "45.77.144.126:3128")
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
    if not proxy_list:
        texts = {
            'fa': "متأسفانه پروکسی برای این نوع اینترنت موجود نیست.",
            'en': "Sorry, no proxies available for this internet type.",
            'ar': "عذراً، لا توجد بروكسيات متاحة لهذا النوع من الانترنت."
        }
        bot.send_message(chat_id, texts[lang_code])
        return
    texts = {
        'fa': "پروکسی‌های مناسب برای اینترنت شما:\n\n",
        'en': "Suitable proxies for your internet:\n\n",
        'ar': "البروكسيات المناسبة لانترنتك:\n\n"
    }
    text = texts[lang_code]
    for i, (primary, secondary) in enumerate(proxy_list, 1):
        text += f"{i}. Primary: {primary}\n   Secondary: {secondary}\n\n"
    bot.send_message(chat_id, text, reply_markup=InlineKeyboardMarkup().add(
        InlineKeyboardButton({'fa':'آموزش','en':'Tutorial','ar':'تعليم'}[lang_code], callback_data="show_tutorial")
    ))

def send_tutorial(chat_id, lang_code, internet_code):
    texts = {
        'fa': f"""آموزش تنظیم DNS Changer برای اینترنت {internet_types[internet_code]['fa']}:
1. اپلیکیشن DNS Changer را از گوگل پلی یا بازار نصب کنید.
2. اپلیکیشن را باز کنید.
3. در قسمت Primary DNS، آدرس پروکسی اول را وارد کنید.
4. در قسمت Secondary DNS، آدرس پروکسی دوم را وارد کنید.
5. روی دکمه Start کلیک کنید تا اتصال فعال شود.
6. برای قطع اتصال روی Stop کلیک کنید.
توجه: حتما تنظیمات اینترنت گوشی شما فعال باشد.""",
        'en': f"""Tutorial for setting up DNS Changer on {internet_types[internet_code]['en']} internet:
1. Install DNS Changer app from Google Play or App Store.
2. Open the app.
3. Enter primary proxy address in Primary DNS field.
4. Enter secondary proxy address in Secondary DNS field.
5. Tap Start to activate connection.
6. Tap Stop to disconnect.
Note: Ensure your phone internet settings are enabled.""",
        'ar': f"""تعليم إعداد DNS Changer لانترنت {internet_types[internet_code]['ar']}:
1. ثبت تطبيق DNS Changer من Google Play أو App Store.
2. افتح التطبيق.
3. أدخل البروكسي الأساسي في حقل Primary DNS.
4. أدخل البروكسي الثانوي في حقل Secondary DNS.
5. اضغط Start لتفعيل الاتصال.
6. اضغط Stop لقطع الاتصال.
ملاحظة: تأكد من تفعيل إعدادات الانترنت في هاتفك."""
    }
    bot.send_message(chat_id, texts[lang_code])

@bot.message_handler(commands=['start'])
def start(message):
    user_data[message.chat.id] = {}
    bot.send_message(message.chat.id, "لطفا زبان مورد نظر خود را انتخاب کنید / Please choose your language / الرجاء اختيار اللغة:", reply_markup=language_keyboard())

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    data = call.data

    if data.startswith("lang_"):
        lang_code = data.split("_")[1]
        user_data[chat_id]['lang'] = lang_code
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                              text={
                                  'fa': 'لطفا نوع اینترنت خود را انتخاب کنید:',
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

bot.infinity_polling()
