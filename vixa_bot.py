from flask import Flask, request
import requests
import os

app = Flask(__name__)

# توکن ربات بله رو اینجا بذار
TOKEN = os.environ.get("1776281842:MYKuAXCjDbOg9vUJbhvM2rEY1VT7QbSRoaLpxlVO")
API_URL = f"https://tapi.bale.ai/bot{TOKEN}"

def send_message(chat_id, text, reply_markup=None):
    data = {
        "chat_id": chat_id,
        "text": text
    }
    if reply_markup:
        data["reply_markup"] = reply_markup
    requests.post(f"{API_URL}/sendMessage", json=data)

def make_inline_keyboard(buttons):
    return {
        "inline_keyboard": [[{"text": text, "callback_data": data}] for text, data in buttons]
    }

@app.route("/", methods=["POST"])
def webhook():
    data = request.json

    if 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '')

        if text == "/start":
            keyboard = make_inline_keyboard([
                ("🎯 دریافت DNS", "get_dns")
            ])
            send_message(chat_id, "سلام! 👋\nبه ربات تنظیم DNS خوش اومدی.\nبا این ربات می‌تونی دی‌ان‌اس‌های مخصوص عبور از فیلترینگ رو دریافت کنی.", keyboard)

    elif 'callback_query' in data:
        chat_id = data['callback_query']['message']['chat']['id']
        data_key = data['callback_query']['data']

        if data_key == 'get_dns':
            dns_list = """🔐 بهترین DNS برای عبور از فیلترینگ:

1️⃣ Cloudflare: 1.1.1.1 / 1.0.0.1  
2️⃣ NextDNS: 45.90.28.0 / 45.90.30.0  
3️⃣ AdGuard: 94.140.14.14 / 94.140.15.15  
4️⃣ Alternate: 76.76.19.19 / 76.223.122.150  
5️⃣ OpenDNS: 208.67.222.222 / 208.67.220.220
"""
            send_message(chat_id, dns_list)

            keyboard = make_inline_keyboard([
                ("📘 آموزش تنظیم DNS", "how_to")
            ])
            send_message(chat_id, "برای دیدن آموزش تنظیم DNS روی گوشی، دکمه زیر رو بزن:", keyboard)

        elif data_key == "how_to":
            keyboard = make_inline_keyboard([
                ("📱 اندروید", "android"),
                ("🍏 آیفون", "ios")
            ])
            send_message(chat_id, "نوع گوشی‌ات رو انتخاب کن:", keyboard)

        elif data_key == "android":
            send_message(chat_id, """📱 آموزش تنظیم DNS در اندروید:

1. نصب اپ DNS Changer از Google Play:  
🔗 https://play.google.com/store/apps/details?id=com.burakgon.dnschanger

2. اجرای برنامه و وارد کردن DNS:  
Primary: 1.1.1.1  
Secondary: 1.0.0.1

3. روی Start بزن ✅  
حالا فیلترینگ تا حدی دور زده می‌شه.
""")

        elif data_key == "ios":
            send_message(chat_id, """🍏 آموزش تنظیم DNS در آیفون:

1. برو به Settings → Wi-Fi  
2. روی شبکه وای‌فای بزن  
3. روی Configure DNS بزن → Manual  
4. DNSها رو وارد کن:  
    - 1.1.1.1  
    - 1.0.0.1  
5. Save رو بزن ✅

DNS حالا روی آیفون تنظیم شده.
""")

    return "ok"

# اجرای ربات روی پورت صحیح برای Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
