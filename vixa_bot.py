import os
from flask import Flask, request
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = os.getenv('7898327343:AAHfKAfWghG7c8Kn8DDSz3ouWdbblLx7_QY')
WEBHOOK_URL_BASE = os.getenv('https://core.telegram.org/bots/api')
WEBHOOK_URL_PATH = f"/{API_TOKEN}/"

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# داده‌ها (زبان‌ها و موضوعات)
languages = {
    'fa': 'فارسی 🇮🇷',
    'en': 'English 🇺🇸',
    'ar': 'العربية 🇸🇦'
}

topics = {
    'python': {
        'fa': ["پایتون یه زبان برنامه‌نویسی باحال و محبوبه 🐍", 
               "می‌تونی باهاش بازی بسازی 🎮", 
               "کتابخانه‌های زیادی داره 📚", 
               "برای هوش مصنوعی عالیه 🤖", 
               "و تازه خیلی آسونه یاد گرفتن! 👍"],
        'en': ["Python is a cool and popular programming language 🐍", 
               "You can make games with it 🎮", 
               "It has many libraries 📚", 
               "Great for AI development 🤖", 
               "And it’s really easy to learn! 👍"],
        'ar': ["بايثون لغة برمجة رائعة وشهيرة 🐍", 
               "يمكنك صنع ألعاب بها 🎮", 
               "لديها مكتبات كثيرة 📚", 
               "ممتازة للذكاء الاصطناعي 🤖", 
               "وسهلة التعلم حقًا! 👍"]
    },
    'general': {
        'fa': ["دنیای ما پر از چیزای عجیب و جالبه 🌍", 
               "آدم‌ها همیشه دنبال یادگیری هستن 📖", 
               "تکنولوژی هر روز پیشرفته‌تر میشه 🤖", 
               "کتابخونه‌ها بهترین دوست‌ها هستن 📚", 
               "و خنده و شوخی همیشه خوبه 😄"],
        'en': ["Our world is full of strange and interesting things 🌍", 
               "People always seek to learn 📖", 
               "Technology gets more advanced every day 🤖", 
               "Libraries are best friends 📚", 
               "And laughter & jokes are always good 😄"],
        'ar': ["عالمنا مليء بالأشياء الغريبة والمثيرة 🌍", 
               "الناس دائمًا يسعون للتعلم 📖", 
               "التكنولوجيا تتطور كل يوم 🤖", 
               "المكتبات هي أفضل الأصدقاء 📚", 
               "والضحك والمزاح دائماً جيد 😄"]
    },
    'history': {
        'fa': ["تاریخ پر از قصه‌های عجیب و غریبه 📜", 
               "بعضی شاه‌ها واقعا شاهکار بودن 👑", 
               "جنگ‌ها همیشه درس‌های بزرگی دارن ⚔️", 
               "تمدن‌های قدیمی خیلی پیشرفته بودن 🏺", 
               "و هیچ‌وقت از یادگیری تاریخ خسته نشو! 📚"],
        'en': ["History is full of strange stories 📜", 
               "Some kings were real legends 👑", 
               "Wars always teach big lessons ⚔️", 
               "Ancient civilizations were very advanced 🏺", 
               "And never get tired of learning history! 📚"],
        'ar': ["التاريخ مليء بالقصص الغريبة 📜", 
               "بعض الملوك كانوا أساطير حقيقية 👑", 
               "الحروب دائماً تعلم دروس كبيرة ⚔️", 
               "الحضارات القديمة كانت متقدمة جداً 🏺", 
               "ولا تتعب من تعلم التاريخ أبداً! 📚"]
    }
}

questions = {
    'python': {
        'fa': [
            ("پایتون برای چه کاری استفاده میشه؟", ["بازی سازی", "پخت کیک", "شنا", "خوابیدن"], 0),
            ("نماد معروف پایتون چیه؟", ["مار 🐍", "گربه 🐱", "سگ 🐶", "پرنده 🐦"], 0),
            ("کدوم گزینه کتابخانه پایتونه؟", ["NumPy", "فیفا", "توییتر", "گوگل"], 0),
            ("پایتون چه زبانیه؟", ["برنامه‌نویسی", "موسیقی", "ورزش", "طبیعت"], 0),
            ("آیا پایتون آسونه؟", ["آره 😎", "نه 🤡", "نمیدونم 😐", "شاید 🤔"], 0)
        ],
        'en': [
            ("What is Python mainly used for?", ["Game making", "Baking", "Swimming", "Sleeping"], 0),
            ("What is the famous Python symbol?", ["Snake 🐍", "Cat 🐱", "Dog 🐶", "Bird 🐦"], 0),
            ("Which one is a Python library?", ["NumPy", "FIFA", "Twitter", "Google"], 0),
            ("What kind of language is Python?", ["Programming", "Music", "Sports", "Nature"], 0),
            ("Is Python easy?", ["Yes 😎", "No 🤡", "I don’t know 😐", "Maybe 🤔"], 0)
        ],
        'ar': [
            ("ما هو الاستخدام الرئيسي لبايثون؟", ["صنع الألعاب", "الخبز", "السباحة", "النوم"], 0),
            ("ما هو رمز بايثون الشهير؟", ["ثعبان 🐍", "قط 🐱", "كلب 🐶", "طائر 🐦"], 0),
            ("أي واحد مكتبة بايثون؟", ["NumPy", "فيفا", "تويتر", "جوجل"], 0),
            ("ما نوع لغة بايثون؟", ["برمجة", "موسيقى", "رياضة", "طبيعة"], 0),
            ("هل بايثون سهلة؟", ["نعم 😎", "لا 🤡", "لا أعرف 😐", "ربما 🤔"], 0)
        ]
    },
    # برای ساده‌سازی، فقط پایتون سوال گذاشتم. می‌تونید خودت اضافه کنی.
}

# ساخت کیبورد زبان
def language_keyboard():
    kb = InlineKeyboardMarkup(row_width=3)
    for code, name in languages.items():
        kb.add(InlineKeyboardButton(name, callback_data=f"lang_{code}"))
    return kb

# کیبورد موضوع
def topic_keyboard(lang_code):
    kb = InlineKeyboardMarkup(row_width=3)
    kb.add(
        InlineKeyboardButton({'fa':"آموزش پایتون 🐍", 'en':"Python Tutorial 🐍", 'ar':"تعليم بايثون 🐍"}[lang_code], callback_data="topic_python"),
        InlineKeyboardButton({'fa':"اطلاعات عمومی 🌍", 'en':"General Knowledge 🌍", 'ar':"المعرفة العامة 🌍"}[lang_code], callback_data="topic_general"),
        InlineKeyboardButton({'fa':"تاریخ 📜", 'en':"History 📜", 'ar':"التاريخ 📜"}[lang_code], callback_data="topic_history")
    )
    return kb

def question_keyboard(lang_code, answers):
    kb = InlineKeyboardMarkup(row_width=2)
    for i, ans in enumerate(answers):
        kb.add(InlineKeyboardButton(ans, callback_data=f"answer_{i}"))
    return kb

user_data = {}

@app.route(f"/{API_TOKEN}/", methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'step': 'choose_language'}
    bot.send_message(chat_id, "😎 سلام رفیق! لطفا زبونت رو انتخاب کن:\nChoose your language, please:\nاختر لغتك، من فضلك:", reply_markup=language_keyboard())

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    data = call.data

    if chat_id not in user_data:
        user_data[chat_id] = {}

    if data.startswith("lang_"):
        lang = data.split("_")[1]
        user_data[chat_id] = {'lang': lang, 'step': 'choose_topic'}
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                              text={
                                  'fa': "😂 خوب! موضوع مورد نظرتو انتخاب کن:",
                                  'en': "😂 Cool! Choose your topic:",
                                  'ar': "😂 حلو! اختر الموضوع:"
                              }[lang],
                              reply_markup=topic_keyboard(lang))

    elif data.startswith("topic_"):
        topic = data.split("_")[1]
        lang = user_data[chat_id].get('lang', 'fa')
        user_data[chat_id].update({'topic': topic, 'step': 'teaching', 'lesson_index': 0, 'score': 0, 'question_index': 0})
        # شروع آموزش
        lesson_text = topics[topic][lang][0]
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                              text=f"📚 {lesson_text} (1/5)",
                              reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                                  {'fa': "بعدی ➡️", 'en': "Next ➡️", 'ar': "التالي ➡️"}[lang], callback_data="next_lesson")))
    elif data == "next_lesson":
        lang = user_data[chat_id].get('lang', 'fa')
        topic = user_data[chat_id].get('topic')
        idx = user_data[chat_id].get('lesson_index', 0) + 1
        if idx < 5:
            user_data[chat_id]['lesson_index'] = idx
            lesson_text = topics[topic][lang][idx]
            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                  text=f"📚 {lesson_text} ({idx+1}/5)",
                                  reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                                      {'fa': "بعدی ➡️", 'en': "Next ➡️", 'ar': "التالي ➡️"}[lang], callback_data="next_lesson")))
        else:
            # شروع سوالات
            user_data[chat_id]['step'] = 'quiz'
            user_data[chat_id]['question_index'] = 0
            lang = user_data[chat_id].get('lang', 'fa')
            q_idx = user_data[chat_id]['question_index']
            q, answers, _ = questions[user_data[chat_id]['topic']][lang][q_idx]
            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                  text=f"❓ سوال 1: {q}",
                                  reply_markup=question_keyboard(lang, answers))
    elif data.startswith("answer_"):
        lang = user_data[chat_id].get('lang', 'fa')
        q_idx = user_data[chat_id].get('question_index', 0)
        topic = user_data[chat_id].get('topic')
        selected = int(data.split("_")[1])
        _, _, correct = questions[topic][lang][q_idx]
        if selected == correct:
            user_data[chat_id]['score'] += 1
            bot.answer_callback_query(call.id, "🎉 آفرین! جواب درست بود 😎")
        else:
            bot.answer_callback_query(call.id, "🙈 اوووه، اشتباه شد! ولی نگران نباش، تلاش کن دوباره 😜")

        # سوال بعدی
        q_idx += 1
        if q_idx < 5:
            user_data[chat_id]['question_index'] = q_idx
            q, answers, _ = questions[topic][lang][q_idx]
            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                  text=f"❓ سوال {q_idx+1}: {q}",
                                  reply_markup=question_keyboard(lang, answers))
        else:
            # پایان آزمون
            score = user_data[chat_id]['score']
            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                  text={
                                      'fa': f"🎉 تبریک! شما {score} از 5 سوال رو درست جواب دادی! 🏆",
                                      'en': f"🎉 Congrats! You got {score} out of 5 right! 🏆",
                                      'ar': f"🎉 مبروك! أجبت {score} من 5 بشكل صحيح! 🏆"
                                  }[lang])
            # می‌تونی اینجا استیکر هم بفرستی
            if score >= 4:
                bot.send_sticker(chat_id, 'CAACAgIAAxkBAAECbRlgxhngclNccdePmH8N0r7xpJ-lWQACkgEAAnK3gUn-kfA-nVY-JSkE')  # استیکر خفن
            else:
                bot.send_sticker(chat_id, 'CAACAgIAAxkBAAECbRpgxhq5H4K1htTQyJcN_2K_Hu3t7QACmwEAAnK3gUm5c2BHZvTAPikE')  # استیکر خنده دار
            user_data[chat_id]['step'] = 'done'

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)
