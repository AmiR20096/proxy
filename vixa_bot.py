from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = "1776281842:MYKuAXCjDbOg9vUJbhvM2rEY1VT7QbSRoaLpxlVO"

API_URL = f'https://tapi.bale.ai/bot{TOKEN}'

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

@app.route('/', methods=['POST'])
def webhook():
    data = request.json

    if 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '')

        if text == '/start':
            keyboard = make_inline_keyboard([
                ("🎯 مشاهده شماره‌های رند", "show_rond"),
                ("🔍 جستجوی شماره خاص", "search_rond"),
                ("🌐 ورود به سایت رندی", "go_site")
            ])
            send_message(chat_id, "سلام! 👋\nبه ربات سیم‌کارت‌های رند خوش آمدی.\nبا این ربات می‌تونی شماره‌های خاص و رند رو ببینی و خریداری کنی.", keyboard)

    elif 'callback_query' in data:
        chat_id = data['callback_query']['message']['chat']['id']
        data_key = data['callback_query']['data']

        if data_key == 'show_rond':
            send_message(chat_id, """📞 نمونه شماره‌های رند ویژه:

🔹 0912-000-0000  
🔹 0912-111-1111  
🔹 0935-555-5555  
🔹 0911-123-1234  

برای مشاهده بیشتر، به سایت زیر برو:
👉 www.rond.ir
""")

        elif data_key == 'search_rond':
            send_message(chat_id, "🔍 لطفاً شماره مورد نظر خود را به صورت کامل یا بخشی از آن وارد کنید (مثلاً: 0912-000):")

        elif data_key == 'go_site':
            send_message(chat_id, "🌐 لینک سایت رسمی خرید شماره رند:\n👉 https://www.rond.ir")

    return "ok"

if __name__ == '__main__':
    app.run()
