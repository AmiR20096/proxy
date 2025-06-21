import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = "7898327343:AAHfKAfWghG7c8Kn8DDSz3ouWdbblLx7_QY"

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🎯 دریافت DNS", callback_data='get_dns'))
    bot.send_message(
        message.chat.id,
        "سلام 👋\nبه ربات تنظیم DNS خوش آمدی!\nبرای دریافت DNS مخصوص عبور از فیلترینگ روی دکمه زیر بزن.",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == 'get_dns')
def send_dns_list(call):
    dns_list = """🔐 بهترین DNSها برای عبور از فیلترینگ و افزایش سرعت:

1️⃣ Cloudflare: 1.1.1.1 / 1.0.0.1  
2️⃣ NextDNS: 45.90.28.0 / 45.90.30.0  
3️⃣ AdGuard DNS: 94.140.14.14 / 94.140.15.15  
4️⃣ Alternate DNS: 76.76.19.19 / 76.223.122.150  
5️⃣ OpenDNS: 208.67.222.222 / 208.67.220.220  
6️⃣ Google DNS: 8.8.8.8 / 8.8.4.4  
7️⃣ Quad9 DNS: 9.9.9.9 / 149.112.112.112
"""
    bot.send_message(call.message.chat.id, dns_list)

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📘 آموزش تنظیم DNS", callback_data='how_to'))
    bot.send_message(call.message.chat.id, "برای دیدن آموزش تنظیم DNS روی گوشی، دکمه زیر رو بزن:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'how_to')
def choose_device(call):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("📱 اندروید", callback_data='android'),
        InlineKeyboardButton("🍏 آیفون", callback_data='ios')
    )
    bot.send_message(call.message.chat.id, "📲 لطفاً نوع گوشی‌ات رو انتخاب کن:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'android')
def android_guide(call):
    bot.send_message(call.message.chat.id, """📱 آموزش تنظیم DNS با برنامه DNS Changer در اندروید:

1. برنامه DNS Changer را از Google Play نصب کن:  
https://play.google.com/store/apps/details?id=com.burakgon.dnschanger

2. برنامه را اجرا کن و DNS ها را به صورت زیر وارد کن:  
Primary DNS: 1.1.1.1  
Secondary DNS: 1.0.0.1

3. روی دکمه Start بزن و اجازه VPN را بده.

اکنون اتصال DNS تغییر کرده و می‌توانی بدون فیلترینگ اینترنت استفاده کنی.
""")

@bot.callback_query_handler(func=lambda call: call.data == 'ios')
def ios_guide(call):
    bot.send_message(call.message.chat.id, """🍏 آموزش تنظیم DNS با برنامه DNS Changer در آیفون:

1. برنامه DNS Changer را از App Store نصب کن.

2. برنامه را اجرا کن.

3. DNS های زیر را وارد کن:  
Primary DNS: 1.1.1.1  
Secondary DNS: 1.0.0.1

4. روی Start بزن و اجازه اتصال VPN را بده.

اکنون DNS تغییر کرده و می‌توانی از اینترنت بدون فیلترینگ استفاده کنی.
""")

bot.infinity_polling()
