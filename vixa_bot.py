import os
from flask import Flask, request
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = os.getenv('7898327343:AAHfKAfWghG7c8Kn8DDSz3ouWdbblLx7_QY')
WEBHOOK_URL_BASE = os.getenv('https://core.telegram.org/bots/api')
WEBHOOK_URL_PATH = f"/{API_TOKEN}/"

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# داده‌های زبان‌ها
languages = {
    'fa': '🇮🇷 فارسی',
    'en': '🇬🇧 English',
    'ar': '🇸🇦 العربية'
}

# موضوعات آموزشی
topics = {
    'python': {'fa': 'پایتون 🐍', 'en': 'Python 🐍', 'ar': 'بايثون 🐍'},
    'general': {'fa': 'اطلاعات عمومی 🧠', 'en': 'General Knowledge 🧠', 'ar': 'معلومات عامة 🧠'},
    'history': {'fa': 'تاریخ 📜', 'en': 'History 📜', 'ar': 'تاريخ 📜'}
}

# محتوا و سوالات (5 درس و 5 سوال برای هر موضوع)
lessons = {
    'python': {
        'fa': [
            "درس ۱: پایتون یه زبان برنامه‌نویسی خیلی ساده‌ست که همه عاشقشن! 😍",
            "درس ۲: متغیرها توی پایتون مثل جعبه‌ست که می‌تونی هرچی خواستی بریزی توش! 📦",
            "درس ۳: شرط‌ها بهت کمک می‌کنن تصمیم بگیری کی چی کار کنه، مثلا اگه گرسنه بودی غذا بخور 🍔",
            "درس ۴: حلقه‌ها یعنی کاری رو چند بار پشت سر هم انجام بدی، مثل تکرار موزیک مورد علاقه‌ت 🎵",
            "درس ۵: توابع بخش‌های کوچیک کد هستن که هر وقت خواستی می‌تونی صداشون کنی 🔊"
        ],
        'en': [
            "Lesson 1: Python is a super simple programming language everyone loves! 😍",
            "Lesson 2: Variables are like boxes where you can put anything you want! 📦",
            "Lesson 3: Conditions help you decide what to do, like if you're hungry, eat 🍔",
            "Lesson 4: Loops let you repeat things multiple times, like your favorite song 🎵",
            "Lesson 5: Functions are small pieces of code you can call whenever you want 🔊"
        ],
        'ar': [
            "الدرس ١: بايثون لغة برمجة سهلة كتير والكل بحبها! 😍",
            "الدرس ٢: المتغيرات مثل صندوق فيك تحط فيه أي شي بدك ياه! 📦",
            "الدرس ٣: الشروط بتساعدك تقرر شو تعمل، مثل إذا كنت جوعان كل 🍔",
            "الدرس ٤: الحلقات بتخليك تعيد الشي كذا مرة، مثل أغنيتك المفضلة 🎵",
            "الدرس ٥: الدوال هي قطع صغيرة من الكود فيك تناديها بأي وقت 🔊"
        ],
        'questions': [
            {
                'fa': ("پایتون یک زبان برنامه‌نویسی است؟", ["درست", "نادرست"], 0),
                'en': ("Python is a programming language?", ["True", "False"], 0),
                'ar': ("هل بايثون لغة برمجة؟", ["صحيح", "خطأ"], 0)
            },
            {
                'fa': ("متغیرها برای ذخیره داده‌ها استفاده می‌شوند؟", ["درست", "نادرست"], 0),
                'en': ("Variables are used to store data?", ["True", "False"], 0),
                'ar': ("المتغيرات تستخدم لتخزين البيانات؟", ["صحيح", "خطأ"], 0)
            },
            {
                'fa': ("شرط‌ها به برنامه می‌گویند چه کاری انجام دهد؟", ["درست", "نادرست"], 0),
                'en': ("Conditions tell the program what to do?", ["True", "False"], 0),
                'ar': ("الشروط بتخبر البرنامج شو يعمل؟", ["صحيح", "خطأ"], 0)
            },
            {
                'fa': ("حلقه‌ها برای تکرار دستورات استفاده می‌شوند؟", ["درست", "نادرست"], 0),
                'en': ("Loops are used to repeat commands?", ["True", "False"], 0),
                'ar': ("الحلقات تستخدم لتكرار الأوامر؟", ["صحيح", "خطأ"], 0)
            },
            {
                'fa': ("توابع بخش‌هایی از کد هستند؟", ["درست", "نادرست"], 0),
                'en': ("Functions are parts of code?", ["True", "False"], 0),
                'ar': ("الدوال هي أجزاء من الكود؟", ["صحيح", "خطأ"], 0)
            },
        ]
    },
    'general': {
        'fa': [
            "درس ۱: زمین گرد است و همه‌مون روش زندگی می‌کنیم 🌍",
            "درس ۲: خورشید از ستاره‌هاست که نور و گرما می‌دهد ☀️",
            "درس ۳: آب برای زندگی لازم است و بدن ما ۷۰٪ آب دارد 💧",
            "درس ۴: هوا چیزی است که ما تنفس می‌کنیم و بدونش نمی‌تونیم باشیم 🌬️",
            "درس ۵: گیاهان با فتوسنتز غذا درست می‌کنند 🌿"
        ],
        'en': [
            "Lesson 1: The Earth is round and we all live on it 🌍",
            "Lesson 2: The Sun is a star that gives light and heat ☀️",
            "Lesson 3: Water is necessary for life and our body is 70% water 💧",
            "Lesson 4: Air is what we breathe and can't live without it 🌬️",
            "Lesson 5: Plants make food with photosynthesis 🌿"
        ],
        'ar': [
            "الدرس ١: الأرض كروية وكلنا عايشين عليها 🌍",
            "الدرس ٢: الشمس نجم بيعطي ضوء وحرارة ☀️",
            "الدرس ٣: الماء ضروري للحياة وجسمنا ٧٠٪ ماء 💧",
            "الدرس ٤: الهواء هو يلي منتنفسه وما فينا نعيش بدونه 🌬️",
            "الدرس ٥: النباتات بتصنع أكل عن طريق البناء الضوئي 🌿"
        ],
        'questions': [
            {
                'fa': ("زمین گرد است؟", ["درست", "نادرست"], 0),
                'en': ("The Earth is round?", ["True", "False"], 0),
                'ar': ("هل الأرض كروية؟", ["صحيح", "خطأ"], 0)
            },
            {
                'fa': ("خورشید یک ستاره است؟", ["درست", "نادرست"], 0),
                'en': ("The Sun is a star?", ["True", "False"], 0),
                'ar': ("هل الشمس نجم؟", ["صحيح", "خطأ"], 0)
            },
            {
                'fa': ("بدن انسان ۷۰٪ آب دارد؟", ["درست", "نادرست"], 0),
                'en': ("Human body is 70% water?", ["True", "False"], 0),
                'ar': ("هل جسم الإنسان ٧٠٪ ماء؟", ["صحيح", "خطأ"], 0)
            },
            {
                'fa': ("هوا چیزی است که تنفس می‌کنیم؟", ["درست", "نادرست"], 0),
                'en': ("Air is what we breathe?", ["True", "False"], 0),
                'ar': ("هل الهواء هو يلي منتنفسه؟", ["صحيح", "خطأ"], 0)
            },
            {
                'fa': ("گیاهان فتوسنتز می‌کنند؟", ["درست", "نادرست"], 0),
                'en': ("Plants do photosynthesis?", ["True", "False"], 0),
                'ar': ("هل النباتات بتعمل البناء الضوئي؟", ["صحيح", "خطأ"], 0)
            },
        ]
    },
    'history': {
        'fa': [
            "درس ۱: تاریخ یعنی داستان زندگی آدم‌ها و اتفاقات گذشته 📜",
            "درس ۲: اولین انسان‌ها میلیون‌ها سال پیش زندگی می‌کردند 🦴",
            "درس ۳: تمدن‌های بزرگی مثل مصر و ایران خیلی قدیمی هستند 🏺",
            "درس ۴: جنگ‌ها و صلح‌ها بخش مهمی از تاریخ هستند ⚔️✌️",
            "درس ۵: ما از تاریخ می‌آموزیم که اشتباهات گذشته را تکرار نکنیم 📚"
        ],
        'en': [
            "Lesson 1: History is the story of people and past events 📜",
            "Lesson 2: The first humans lived millions of years ago 🦴",
            "Lesson 3: Great civilizations like Egypt and Iran are very old 🏺",
            "Lesson 4: Wars and peace are important parts of history ⚔️✌️",
            "Lesson 5: We learn from history not to repeat past mistakes 📚"
        ],
        'ar': [
            "الدرس ١: التاريخ هو قصة الناس والأحداث الماضية 📜",
            "الدرس ٢: أول البشر عاشوا من ملايين السنين 🦴",
            "الدرس ٣: حضارات عظيمة مثل مصر وإيران قديمة كتير 🏺",
            "الدرس ٤: الحروب والسلام جزء مهم من التاريخ ⚔️✌️",
            "الدرس ٥: بنتعلم من التاريخ ما نعيد أخطاء الماضي 📚"
        ],
        'questions': [
            {
                'fa': ("تاریخ داستان زندگی آدم‌ها است؟", ["درست", "نادرست"], 0),
                'en': ("History is the story of people?", ["True", "False"], 0),
                'ar': ("هل التاريخ قصة الناس؟", ["صحيح", "خطأ"], 0)
            },
            {
                'fa': ("اولین انسان‌ها میلیون‌ها سال پیش بودند؟", ["درست", "نادرست"], 0),
                'en': ("First humans lived millions of years ago?", ["True", "False"], 0),
                'ar': ("هل أول البشر عاشوا من ملايين السنين؟", ["صحيح", "خطأ"], 0)
            },
            {
                'fa': ("تمدن مصر قدیمی است؟", ["درست", "نادرست"], 0),
                'en': ("Egypt civilization is old?", ["True", "False"], 0),
                'ar': ("هل حضارة مصر قديمة؟", ["صحيح", "خطأ"], 0)
            },
            {
                'fa': ("جنگ و صلح بخشی از تاریخ هستند؟", ["درست", "نادرست"], 0),
                'en': ("War and peace are parts of history?", ["True", "False"], 0),
                'ar': ("هل الحرب والسلام أجزاء من التاريخ؟", ["صحيح", "خطأ"], 0)
            },
            {
                'fa': ("ما باید از تاریخ یاد بگیریم؟", ["درست", "نادرست"], 0),
                'en': ("We should learn from history?", ["True", "False"], 0),
                'ar': ("هل لازم نتعلم من التاريخ؟", ["صحيح", "خطأ"], 0)
            },
        ]
    }
}

# استیکرها و پاسخ‌های شوخی
stickers = {
    'correct': 'CAACAgIAAxkBAAEBQZ5gQ8lGzoVmvpt-N0H3bqEOV_H8AAJ9AAO8-T4RnQqv5Ym1Mq7iQE',
    'wrong': 'CAACAgIAAxkBAAEBRaFgQ6AvSdHrK7HJk5pBNKu5iSsy8gACiAAPpL0qEmLQpQ2RUrUziQE'
}

funny_correct = {
    'fa': ["وااای چه نابغه‌ای! 😎", "دمت گرم! 🎉", "درست جواب دادی، کُشته شدیم! 😂"],
    'en': ["Wow, you're a genius! 😎", "Nice one! 🎉", "Correct, you rock! 😂"],
    'ar': ["واو، إنت عبقري! 😎", "حلو كتير! 🎉", "صح، إنت رهيب! 😂"]
}

funny_wrong = {
    'fa': ["آخ جوووون، اشتباه شد! 🙈", "دوباره تلاش کن، نشد! 🤪", "نه بابا اشتباهه! 😂"],
    'en': ["Oops, wrong! 🙈", "Try again, no luck! 🤪", "Nope, wrong! 😂"],
    'ar': ["أوه، خطأ! 🙈", "حاول مرة تانية! 🤪", "لا، خطأ! 😂"]
}

# دیتای کاربر برای ذخیره زبان، موضوع، مرحله و امتیاز
user_data = {}

def language_keyboard():
    kb = InlineKeyboardMarkup(row_width=3)
    for code, name in languages.items():
        kb.add(InlineKeyboardButton(name, callback_data=f"lang_{code}"))
    return kb

def topics_keyboard(lang_code):
    kb = InlineKeyboardMarkup(row_width=1)
    for code, names in topics.items():
        kb.add(InlineKeyboardButton(names[lang_code], callback_data=f"topic_{code}"))
    return kb

def question_keyboard(lang_code, options):
    kb = InlineKeyboardMarkup(row_width=2)
    for i, opt in enumerate(options):
        kb.add(InlineKeyboardButton(opt, callback_data=f"answer_{i}"))
    return kb

@app.route(f"/{API_TOKEN}/", methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'stage': 'choose_lang'}
    bot.send_message(chat_id, "🌟 سلام! لطفا زبانت رو انتخاب کن:\n🌟 Please select your language:\n🌟 الرجاء اختيار اللغة:", reply_markup=language_keyboard())

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    data = call.data

    # انتخاب زبان
    if data.startswith("lang_"):
        lang = data.split("_")[1]
        user_data[chat_id] = {
            'lang': lang,
            'stage': 'choose_topic',
            'score': 0,
            'lesson_index': 0,
            'question_index': 0,
            'topic': None
        }
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                              text={"fa": "موضوع مورد نظرت رو انتخاب کن:", "en": "Choose your topic:", "ar": "اختر موضوعك:"}[lang],
                              reply_markup=topics_keyboard(lang))
        return

    # انتخاب موضوع
    if data.startswith("topic_"):
        topic = data.split("_")[1]
        lang = user_data.get(chat_id, {}).get('lang', 'fa')
        user_data[chat_id]['topic'] = topic
        user_data[chat_id]['stage'] = 'lesson'
        user_data[chat_id]['lesson_index'] = 0
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                              text={"fa": f"آموزش شروع میشه... درس ۱:\n\n{lessons[topic][lang][0]}",
                                    "en": f"Starting lesson... Lesson 1:\n\n{lessons[topic][lang][0]}",
                                    "ar": f"نبدأ الدرس... الدرس ١:\n\n{lessons[topic][lang][0]}"}[lang])
        return

    # درس بعدی
    if user_data.get(chat_id, {}).get('stage') == 'lesson':
        topic = user_data[chat_id]['topic']
        lang = user_data[chat_id]['lang']
        idx = user_data[chat_id]['lesson_index'] + 1
        if idx < 5:
            user_data[chat_id]['lesson_index'] = idx
            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                  text=lessons[topic][lang][idx])
        else:
            # رفتن به سوالات
            user_data[chat_id]['stage'] = 'quiz'
            user_data[chat_id]['question_index'] = 0
            idx = 0
            q = lessons[topic]['questions'][idx][lang]
            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                  text=f"حالا ۵ سوال داریم! 🧐\n\n{q[0]}",
                                  reply_markup=question_keyboard(lang, q[1]))
        return

    # پاسخ به سوالات
    if user_data.get(chat_id,
