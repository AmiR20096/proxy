import os
from flask import Flask, request
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# دریافت توکن از متغیر محیطی TELEGRAM_API_TOKEN
API_TOKEN = os.getenv('7898327343:AAHfKAfWghG7c8Kn8DDSz3ouWdbblLx7_QY')
if not API_TOKEN:
    print("لطفا متغیر محیطی TELEGRAM_API_TOKEN را تنظیم کنید!")
    exit(1)

bot = telebot.TeleBot(API_TOKEN)
app = Flask(_name_)

# داده‌های کاربر برای ذخیره زبان و موضوع
user_data = {}

languages = {
    'fa': 'فارسی',
    'en': 'English',
    'ar': 'العربية'
}

subjects = {
    'python': {
        'fa': ['درس ۱: متغیرها 🐍', 'درس ۲: شرط‌ها 🤔', 'درس ۳: حلقه‌ها 🔄', 'درس ۴: توابع 🛠', 'درس ۵: لیست‌ها 📋'],
        'en': ['Lesson 1: Variables 🐍', 'Lesson 2: Conditions 🤔', 'Lesson 3: Loops 🔄', 'Lesson 4: Functions 🛠', 'Lesson 5: Lists 📋'],
        'ar': ['الدرس ١: المتغيرات 🐍', 'الدرس ٢: الشروط 🤔', 'الدرس ٣: الحلقات 🔄', 'الدرس ٤: الدوال 🛠', 'الدرس ٥: القوائم 📋']
    },
    'general': {
        'fa': ['درس ۱: علم و دانش 📚', 'درس ۲: جغرافیا 🌍', 'درس ۳: فناوری ⚙', 'درس ۴: هنر 🎨', 'درس ۵: ورزش ⚽'],
        'en': ['Lesson 1: Science 📚', 'Lesson 2: Geography 🌍', 'Lesson 3: Technology ⚙', 'Lesson 4: Art 🎨', 'Lesson 5: Sports ⚽'],
        'ar': ['الدرس ١: العلوم 📚', 'الدرس ٢: الجغرافيا 🌍', 'الدرس ٣: التكنولوجيا ⚙', 'الدرس ٤: الفن 🎨', 'الدرس ٥: الرياضة ⚽']
    },
    'history': {
        'fa': ['درس ۱: ایران باستان 🏛', 'درس ۲: دوران اسلامی 🕌', 'درس ۳: انقلاب‌ها ⚔', 'درس ۴: جنگ‌های جهانی 🌐', 'درس ۵: تاریخ معاصر 🕰'],
        'en': ['Lesson 1: Ancient Iran 🏛', 'Lesson 2: Islamic Era 🕌', 'Lesson 3: Revolutions ⚔', 'Lesson 4: World Wars 🌐', 'Lesson 5: Modern History 🕰'],
        'ar': ['الدرس ١: إيران القديمة 🏛', 'الدرس ٢: العصر الإسلامي 🕌', 'الدرس ٣: الثورات ⚔', 'الدرس ٤: الحروب العالمية 🌐', 'الدرس ٥: التاريخ الحديث 🕰']
    }
}

questions = {
    'python': {
        'fa': [
            ("متغیر چیست؟ 🤔", ["یک ظرف 🥫", "یک عدد", "یک متن"], 0),
            ("برای شرط استفاده می‌کنیم؟", ["if", "for", "while"], 0),
            ("حلقه چیست؟ 🔄", ["تکرار", "شرط", "توابع"], 0),
            ("چگونه تابع می‌سازیم؟", ["def", "func", "var"], 0),
            ("لیست چیست؟", ["یک مجموعه", "یک عدد", "یک متن"], 0)
        ],
        'en': [
            ("What is a variable? 🤔", ["A container 🥫", "A number", "A text"], 0),
            ("Which keyword for condition?", ["if", "for", "while"], 0),
            ("What is a loop? 🔄", ["Repetition", "Condition", "Function"], 0),
            ("How to define a function?", ["def", "func", "var"], 0),
            ("What is a list?", ["A collection", "A number", "A text"], 0)
        ],
        'ar': [
            ("ما هو المتغير؟ 🤔", ["حاوية 🥫", "عدد", "نص"], 0),
            ("أي كلمة شرط؟", ["if", "for", "while"], 0),
            ("ما هي الحلقة؟ 🔄", ["تكرار", "شرط", "دالة"], 0),
            ("كيف تنشئ دالة؟", ["def", "func", "var"], 0),
            ("ما هي القائمة؟", ["مجموعة", "عدد", "نص"], 0)
        ]
    },
    'general': {
        'fa': [
            ("آب چند درجه می‌جوشد؟", ["۱۰۰", "۵۰", "۲۰۰"], 0),
            ("پایتخت ایران کجاست؟", ["تهران", "مشهد", "اصفهان"], 0),
            ("سیاره ما کدام است؟", ["زمین", "مریخ", "زهره"], 0),
            ("رنگ آسمان چیست؟", ["آبی", "قرمز", "سبز"], 0),
            ("بزرگترین قاره؟", ["آسیا", "آفریقا", "اروپا"], 0)
        ],
        'en': [
            ("At what temperature does water boil?", ["100", "50", "200"], 0),
            ("Capital of Iran?", ["Tehran", "Mashhad", "Isfahan"], 0),
            ("Which planet is ours?", ["Earth", "Mars", "Venus"], 0),
            ("Color of sky?", ["Blue", "Red", "Green"], 0),
            ("Largest continent?", ["Asia", "Africa", "Europe"], 0)
        ],
        'ar': [
            ("عند أي درجة يغلي الماء؟", ["100", "50", "200"], 0),
            ("عاصمة إيران؟", ["طهران", "مشهد", "أصفهان"], 0),
            ("أي كوكب لنا؟", ["الأرض", "المريخ", "الزهرة"], 0),
            ("لون السماء؟", ["أزرق", "أحمر", "أخضر"], 0),
            ("أكبر قارة؟", ["آسيا", "أفريقيا", "أوروبا"], 0)
        ]
    },
    'history': {
        'fa': [
            ("ایران باستان چه دوره‌ای است؟", ["پیش از اسلام", "دوره صفویه", "دوره قاجار"], 0),
            ("انقلاب مشروطه کی بود؟", ["۱۹۰۶", "۱۸۵۰", "۲۰۰۰"], 0),
            ("جنگ جهانی اول کی شروع شد؟", ["۱۹۱۴", "۱۸۹۰", "۱۹۵۰"], 0),
            ("دوره اسلامی چه زمانی است؟", ["پس از ۶۱۰ میلادی", "قبل از ۶۱۰", "پس از ۱۰۰۰"], 0),
            ("تاریخ معاصر به چه معنی است؟", ["صد سال اخیر", "هزار سال پیش", "۵۰ سال پیش"], 0)
        ],
        'en': [
            ("What era is Ancient Iran?", ["Pre-Islamic", "Safavid", "Qajar"], 0),
            ("When was the Constitutional Revolution?", ["1906", "1850", "2000"], 0),
            ("When did WWI start?", ["1914", "1890", "1950"], 0),
            ("When is Islamic Era?", ["After 610 AD", "Before 610", "After 1000"], 0),
            ("What is modern history?", ["Last 100 years", "1000 years ago", "50 years ago"], 0)
        ],
        'ar': [
            ("ما هي حقبة إيران القديمة؟", ["قبل الإسلام", "صفوي", "قاجار"], 0),
            ("متى كانت الثورة الدستورية؟", ["1906", "1850", "2000"], 0),
            ("متى بدأت الحرب العالمية الأولى؟", ["1914", "1890", "1950"], 0),
            ("متى هي الحقبة الإسلامية؟", ["بعد 610 ميلادي", "قبل 610", "بعد 1000"], 0),
            ("ما هو التاريخ الحديث؟", ["100 سنة الماضية", "1000 سنة مضت", "50 سنة مضت"], 0)
        ]
    }
}

stickers = {
    'correct': 'CAACAgIAAxkBAAEHZvlkUo8ajxQJW6_MLQx5bR14Vbr6EgAC3gADVp29CqxCrpMH9Uz1IwQ',
    'wrong': 'CAACAgIAAxkBAAEHZ0VkUo_4rRXAAUPk_Vmt8DbN6vdCZwAC6AADVp29CrzBrCNUhbhkIwQ'
}

def language_keyboard():
    kb = InlineKeyboardMarkup(row_width=3)
    for code, name in languages.items():
        kb.add(InlineKeyboardButton(name, callback_data=f"lang_{code}"))
    return kb

def subject_keyboard(lang_code):
    kb = InlineKeyboardMarkup(row_width=2)
    for subj in subjects.keys():
        name = {
            'fa': {'python':'پایتون', 'general':'اطلاعات عمومی', 'history':'تاریخ'}[subj],
            'en': {'python':'Python', 'general':'General Knowledge', 'history':'History'}[subj],
            'ar': {'python':'بايثون', 'general':'معلومات عامة', 'history':'التاريخ'}[subj]
        }[lang_code]
        kb.add(InlineKeyboardButton(name, callback_data=f"subject_{subj}"))
    return kb

def lessons_keyboard(lang_code, lessons):
    kb = InlineKeyboardMarkup(row_width=1)
    for i, lesson in enumerate(lessons, 1):
        kb.add(InlineKeyboardButton(f"درس {i} 📚", callback_data=f"lesson_{i-1}"))
    kb.add(InlineKeyboardButton({'fa':'سوالات ❓','en':'Questions ❓','ar':'أسئلة ❓'}[lang_code], callback_data="start_questions"))
    return kb

def question_keyboard(lang_code, options):
    kb = InlineKeyboardMarkup(row_width=1)
    for i, opt in enumerate(options):
        kb.add(InlineKeyboardButton(opt, callback_data=f"answer_{i}"))
    return kb

@app.route(f"/{API_TOKEN}", methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}
    bot.send_message(chat_id, "👋 سلام! لطفاً زبانت رو انتخاب کن / Please choose your language / اختر لغتك:", reply_markup=language_keyboard())

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    data = call.data

    if data.startswith("lang_"):
        lang_code = data.split("_")[1]
        user_data[chat_id] = {'lang': lang_code}
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                              text={"fa":"زبان انتخاب شد! حالا موضوع رو انتخاب کن 🧐",
                                    "en":"Language set! Now pick a subject 🧐",
                                    "ar":"تم اختيار اللغة! اختر الموضوع 🧐"}[lang_code],
                              reply_markup=subject_keyboard(lang_code))

    elif data.startswith("subject_"):
        subj = data.split("_")[1]
        lang_code = user_data[chat_id]['lang']
        user_data[chat_id].update({'subject': subj, 'lesson_index': 0, 'score': 0})
        lessons = subjects[subj][lang_code]
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                              text={"fa":"شروع آموزش! درس اول:\n\n" + lessons[0],
                                    "en":"Starting lessons! Lesson 1:\n\n" + lessons[0],
                                    "ar":"بدء الدروس! الدرس ١:\n\n" + lessons[0]}[lang_code],
                              reply_markup=lessons_keyboard(lang_code, lessons))

    elif data.startswith("lesson_"):
        lang_code = user_data[chat_id]['lang']
        subj = user_data[chat_id]['subject']
        idx = int(data.split("_")[1])
        lessons = subjects[subj][lang_code]
        if idx < len(lessons):
            user_data[chat_id]['lesson_index'] = idx
            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                  text={"fa":f"درس {idx+1}:\n\n" + lessons[idx],
                                        "en":f"Lesson {idx+1}:\n\n" + lessons[idx],
                                        "ar":f"الدرس {idx+1}:\n\n" + lessons[idx]}[lang_code],
                                  reply_markup=lessons_keyboard(lang_code, lessons))
        else:
            bot.answer_callback_query(call.id, "هیچ درس جدیدی نیست! / No more lessons! / لا مزيد من الدروس!")

    elif data == "start_questions":
        lang_code = user_data[chat_id]['lang']
        subj = user_data[chat_id]['subject']
        user_data[chat_id]['q_index'] = 0
        user_data[chat_id]['score'] = 0
        send_question(chat_id)

    elif data.startswith("answer_"):
        lang_code = user_data[chat_id]['lang']
        subj = user_data[chat_id]['subject']
        q_idx = user_data[chat_id]['q_index']
        selected = int(data.split("_")[1])
        correct = questions[subj][lang_code][q_idx][2]

        if selected == correct:
            user_data[chat_id]['score'] += 1
            bot.send_sticker(chat_id, stickers['correct'])
            bot.answer_callback_query(call.id, "🙌 آفرین! درست زدی! / Correct! / صح! 🎉")
        else:
            bot.send_sticker(chat_id, stickers['wrong'])
            bot.answer_callback_query(call.id, "🙈 اوووه، اشتباه شد! / Wrong! / خطأ! 😅")

        user_data[chat_id]['q_index'] += 1
        if user_data[chat_id]['q_index'] < len(questions[subj][lang_code]):
            send_question(chat_id)
        else:
            score = user_data[chat_id]['score']
            total = len(questions[subj][lang_code])
            texts = {
                'fa': f"🎉 تبریک! امتیاز شما: {score}/{total} 🎉\n\nمعلومه زرنگی 😉",
                'en': f"🎉 Congrats! Your score: {score}/{total} 🎉\n\nYou’re smart 😉",
                'ar': f"🎉 مبروك! نتيجتك: {score}/{total} 🎉\n\nأنت ذكي 😉"
            }
            bot.send_message(chat_id, texts[lang_code])
            user_data.pop(chat_id, None)

def send_question(chat_id):
    lang_code = user_data[chat_id]['lang']
    subj = user_data[chat_id]['subject']
    q_idx = user_data[chat_id]['q_index']
    q_text, options, _ = questions[subj][lang_code][q_idx]

    bot.send_message(chat_id, q_text, reply_markup=question_keyboard(lang_code, options))

if _name_ == "_main_":
    # دریافت آدرس وبهوک از متغیر محیطی WEBHOOK_URL
    WEBHOOK_URL_BASE = os.getenv('https://core.telegram.org/bots/api')
    if not WEBHOOK_URL_BASE:
        print("لطفا متغیر محیطی WEBHOOK_URL را تنظیم کنید! (مثال: https://yourapp.onrender.com)")
        exit(1)
    WEBHOOK_URL_PATH = f"/{API_TOKEN}"

    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)
    print("✅ ربات با موفقیت با وبهوک اجرا شد!")

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
