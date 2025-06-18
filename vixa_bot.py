import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = "7898327343:AAHfKAfWghG7c8Kn8DDSz3ouWdbblLx7_QY"
bot = telebot.TeleBot(API_TOKEN)

user_data = {}

languages = {
    'fa': '🇮🇷 فارسی',
    'en': '🇺🇸 English',
    'ar': '🇸🇦 العربية'
}

topics = {
    'python': {'fa':'🐍 آموزش پایتون', 'en':'🐍 Python Lessons', 'ar':'🐍 دروس بايثون'},
    'general': {'fa':'🧠 اطلاعات عمومی', 'en':'🧠 General Knowledge', 'ar':'🧠 المعرفة العامة'},
    'history': {'fa':'📜 تاریخ', 'en':'📜 History', 'ar':'📜 التاريخ'}
}

# پیام‌ها به سه زبان (با طنز و ایموجی)
texts = {
    'start': {
        'fa': "🤣🤣 سلام! اول یه زبون انتخاب کن که من باهات حال کنم!",
        'en': "🤣🤣 Hey! Pick a language so I can vibe with you!",
        'ar': "🤣🤣 هلا! أولاً اختار اللغة عشان نضحك سوى!"
    },
    'choose_topic': {
        'fa': "🔥 موضوع رو انتخاب کن که بترکونی!",
        'en': "🔥 Choose a topic to rock!",
        'ar': "🔥 اختر موضوع عشان تكون فنان!"
    },
    'lesson_intro': {
        'fa': "📚 بفرما آموزش‌ها! آماده برای خفن بازی؟ 😁",
        'en': "📚 Here are your lessons! Ready to be awesome? 😁",
        'ar': "📚 هذه دروسك! جاهز لتكون رائع؟ 😁"
    },
    'question_intro': {
        'fa': "❓ سوال‌ها میان! جواب بده وگرنه مسخره‌ات می‌کنم 😂",
        'en': "❓ Questions coming! Answer or I roast you 😂",
        'ar': "❓ الأسئلة جاية! جاوب وإلا رح أسخرك 😂"
    },
    'score_good': {
        'fa': "🌟 تو نابغی! ستاره‌ی منی! ⭐️⭐️⭐️",
        'en': "🌟 You're a genius! My star! ⭐️⭐️⭐️",
        'ar': "🌟 أنت عبقري! نجمتي! ⭐️⭐️⭐️"
    },
    'score_ok': {
        'fa': "👏 خوب بود، بهتر از اینم می‌تونی!",
        'en': "👏 Good job, you can do better!",
        'ar': "👏 عمل جيد، يمكنك أن تكون أفضل!"
    },
    'score_bad': {
        'fa': "😂 اوووه، بیا یه قهوه بخور و دوباره تلاش کن!",
        'en': "😂 Oh no, grab a coffee and try again!",
        'ar': "😂 أوه لا، اشرب قهوة وحاول مرة أخرى!"
    }
}

# آموزش‌ها به سه زبان (هر موضوع 5 آموزش)
lessons = {
    'python': {
        'fa': [
            "👨‍💻 پایتون مثل موزیک رپ جذابه! شروع کن با print('سلام دنیا') 😎",
            "🔍 متغیرها مثل جیب‌پول تو هستند!",
            "🎯 شرط‌ها مثل پلیس راهنمایی: if/else",
            "🔄 حلقه‌ها مثل چرخ و فلک!",
            "📚 فانکشن‌ها مثل ربات‌های دستیار!"
        ],
        'en': [
            "👨‍💻 Python is like rap music! Start with print('Hello World') 😎",
            "🔍 Variables are like your wallet!",
            "🎯 Conditions are like traffic cops: if/else",
            "🔄 Loops are like a carousel!",
            "📚 Functions are like assistant robots!"
        ],
        'ar': [
            "👨‍💻 بايثون مثل الراب! ابدأ بـ print('مرحبا بالعالم') 😎",
            "🔍 المتغيرات مثل محفظتك!",
            "🎯 الشروط مثل رجال المرور: if/else",
            "🔄 الحلقات مثل الدوامة!",
            "📚 الدوال مثل الروبوتات المساعدة!"
        ]
    },
    'general': {
        'fa': [
            "🌍 زمین گرده، بعضیا هنوز فکر می‌کنن صافه!",
            "🚀 اولین انسان روی ماه نیل آرمسترانگ بود!",
            "📱 گوشی هوشمند ۲۵ سال پیش نبود!",
            "🍕 پیتزا از ایتالیاست!",
            "🧠 مغز انسان سریع‌تر از اینترنت 5G است!"
        ],
        'en': [
            "🌍 Earth is round, some still think it's flat!",
            "🚀 Neil Armstrong was first on the moon!",
            "📱 Smartphones didn't exist 25 years ago!",
            "🍕 Pizza is from Italy!",
            "🧠 The brain is faster than 5G internet!"
        ],
        'ar': [
            "🌍 الأرض مستديرة، والبعض لا يصدق!",
            "🚀 نيل آرمسترونغ كان أول من وصل للقمر!",
            "📱 الهواتف الذكية لم تكن موجودة منذ 25 سنة!",
            "🍕 البيتزا من إيطاليا!",
            "🧠 الدماغ أسرع من إنترنت 5G!"
        ]
    },
    'history': {
        'fa': [
            "🏺 مصر باستان پر از راز!",
            "⚔️ جنگ‌های صلیبی داستان خون و دود!",
            "👑 شاهان قدیم استرس داشتند!",
            "🕰️ ساعت اختراع شد تا دیر نکنیم!",
            "🚢 کشتی تایتانیک داستان غرق شدن!"
        ],
        'en': [
            "🏺 Ancient Egypt full of secrets!",
            "⚔️ Crusades were bloody wars!",
            "👑 Old kings were stressed!",
            "🕰️ Clocks invented to stop being late!",
            "🚢 Titanic was a sinking story!"
        ],
        'ar': [
            "🏺 مصر القديمة مليئة بالأسرار!",
            "⚔️ الحروب الصليبية كانت دموية!",
            "👑 الملوك القدماء كانوا متوترين!",
            "🕰️ اخترعوا الساعة لعدم التأخير!",
            "🚢 قصة غرق التايتانيك!"
        ]
    }
}

# سوالات به سه زبان: هر سوال به صورت (سوال, [جواب‌ها], جواب_درست_اندیس)
questions = {
    'python': {
        'fa': [
            ("print('سلام') چه کاری می‌کند؟", ['سلام را چاپ می‌کند', 'صدا می‌دهد', 'هیچ کاری نمی‌کند'], 0),
            ("کدام متغیر درست است؟", ['1number', 'number1', 'number-1'], 1),
            ("for چیست؟", ['حلقه', 'متغیر', 'تابع'], 0),
            ("تابع چیست؟", ['کد تکراری', 'دستور شرطی', 'نوع داده'], 0),
            ("کدام نماد برای نظر است؟", ['#', '//', '/*'], 0)
        ],
        'en': [
            ("What does print('Hello') do?", ['Prints Hello', 'Makes sound', 'Does nothing'], 0),
            ("Which variable name is correct?", ['1number', 'number1', 'number-1'], 1),
            ("What is 'for'?", ['Loop', 'Variable', 'Function'], 0),
            ("What is a function?", ['Reusable code', 'Condition', 'Data type'], 0),
            ("Which symbol is comment?", ['#', '//', '/*'], 0)
        ],
        'ar': [
            ("ماذا يفعل print('مرحبا')؟", ['يطبع مرحبا', 'يصدر صوت', 'لا يفعل شيئاً'], 0),
            ("أي اسم متغير صحيح؟", ['1number', 'number1', 'number-1'], 1),
            ("ما هو 'for'؟", ['حلقة', 'متغير', 'دالة'], 0),
            ("ما هي الدالة؟", ['كود قابل لإعادة الاستخدام', 'شرط', 'نوع بيانات'], 0),
            ("أي رمز للتعليق؟", ['#', '//', '/*'], 0)
        ]
    },
    'general': {
        'fa': [
            ("اولین ماه‌نورد کی بود؟", ['نیل آرمسترانگ', 'یوری گاگارین', 'فضانورد بازنشسته'], 0),
            ("زمین گرد است یا صاف؟", ['صاف', 'گرد', 'مربع'], 1),
            ("اولین تلفن همراه کی ساخته شد؟", ['1983', '1990', '2000'], 0),
            ("پیتزا از کجاست؟", ['ایتالیا', 'فرانسه', 'آلمان'], 0),
            ("مغز چقدر سریع است؟", ['کند', 'سریع', 'متوسط'], 1)
        ],
        'en': [
            ("Who was the first moonwalker?", ['Neil Armstrong', 'Yuri Gagarin', 'Retired astronaut'], 0),
            ("Is Earth flat or round?", ['Flat', 'Round', 'Square'], 1),
            ("When was the first mobile phone made?", ['1983', '1990', '2000'], 0),
            ("Where is pizza from?", ['Italy', 'France', 'Germany'], 0),
            ("How fast is the brain?", ['Slow', 'Fast', 'Medium'], 1)
        ],
        'ar': [
            ("من كان أول من مشى على القمر؟", ['نيل آرمسترونغ', 'يوري غاغارين', 'رائد فضاء متقاعد'], 0),
            ("هل الأرض مسطحة أم مستديرة؟", ['مسطحة', 'مستديرة', 'مربعة'], 1),
            ("متى تم صنع أول هاتف محمول؟", ['1983', '1990', '2000'], 0),
            ("من أين تأتي البيتزا؟", ['إيطاليا', 'فرنسا', 'ألمانيا'], 0),
            ("ما سرعة الدماغ؟", ['بطيء', 'سريع', 'متوسط'], 1)
        ]
    },
    'history': {
        'fa': [
            ("مومیایی‌ها متعلق به کدام کشورند؟", ['مصر', 'یونان', 'ایران'], 0),
            ("جنگ‌های صلیبی مربوط به چه قرنی است؟", ['قرن 11', 'قرن 15', 'قرن 19'], 0),
            ("کدام شاه قدیم نبود؟", ['کوروش', 'الکساندر', 'پادشاه فوتبال'], 2),
            ("ساعت برای چه اختراع شد؟", ['تنظیم زمان', 'فروش', 'تزئین'], 0),
            ("تایتانیک چه بود؟", ['کشتی', 'هواپیما', 'قطار'], 0)
        ],
        'en': [
            ("Mummies belong to which country?", ['Egypt', 'Greece', 'Iran'], 0),
            ("The Crusades happened in which century?", ['11th', '15th', '19th'], 0),
            ("Which one was NOT an old king?", ['Cyrus', 'Alexander', 'Football King'], 2),
            ("Why was the clock invented?", ['To tell time', 'For sale', 'Decoration'], 0),
            ("What was Titanic?", ['Ship', 'Plane', 'Train'], 0)
        ],
        'ar': [
            ("إلى أي دولة تنتمي المومياوات؟", ['مصر', 'اليونان', 'إيران'], 0),
            ("في أي قرن حدثت الحروب الصليبية؟", ['الحادي عشر', 'الخامس عشر', 'التاسع عشر'], 0),
            ("أيهم لم يكن ملكاً قديماً؟", ['كورش', 'الإسكندر', 'ملك كرة القدم'], 2),
            ("لماذا اخترع الساعة؟", ['لتحديد الوقت', 'للبيع', 'للزينة'], 0),
            ("ما هو التايتانيك؟", ['سفينة', 'طائرة', 'قطار'], 0)
        ]
    }
}

stickers = {
    'good': 'CAACAgIAAxkBAAEFq1JkDjQl_Jr9q5tTzYmICZy-0lyRAwAC3QADr8ZSGwPfuZ1U_4aQHgQ',
    'bad': 'CAACAgIAAxkBAAEFq1NkDjS-NHvhC8zGCHH3br4ONNg3CQACBAADr8ZSGzBPaSWwsOaMHgQ'
}

def lang_markup():
    markup = InlineKeyboardMarkup(row_width=3)
    for code, name in languages.items():
        markup.add(InlineKeyboardButton(name, callback_data=f'lang_{code}'))
    return markup

def topic_markup(lang):
    markup = InlineKeyboardMarkup(row_width=2)
    for key in topics.keys():
        markup.add(InlineKeyboardButton(topics[key][lang], callback_data=f'topic_{key}'))
    return markup

def next_lesson_markup(idx, total, lang):
    markup = InlineKeyboardMarkup()
    if idx < total -1:
        # متن دکمه بعدی به زبان انتخابی
        btn_text = {'fa':'📖 بعدی', 'en':'📖 Next', 'ar':'📖 التالي'}[lang]
        markup.add(InlineKeyboardButton(btn_text, callback_data=f'lesson_{idx+1}'))
    else:
        btn_text = {'fa':'❓ برو سراغ سوال', 'en':'❓ Go to Questions', 'ar':'❓ اذهب للأسئلة'}[lang]
        markup.add(InlineKeyboardButton(btn_text, callback_data='start_questions'))
    return markup

def question_markup(q_idx, answers):
    markup = InlineKeyboardMarkup()
    for i, ans in enumerate(answers):
        markup.add(InlineKeyboardButton(ans, callback_data=f'answer_{q_idx}_{i}'))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    user_data[message.chat.id] = {'score':0}
    bot.send_message(message.chat.id, texts['start']['fa'], reply_markup=lang_markup())

@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def select_language(call):
    lang = call.data.split('_')[1]
    user_data[call.message.chat.id]['lang'] = lang
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f"👍 {languages[lang]} انتخاب شد!\n\n{texts['choose_topic'][lang]}",
                          reply_markup=topic_markup(lang))

@bot.callback_query_handler(func=lambda call: call.data.startswith('topic_'))
def select_topic(call):
    topic = call.data.split('_')[1]
    chat_id = call.message.chat.id
    lang = user_data[chat_id]['lang']
    user_data[chat_id]['topic'] = topic
    user_data[chat_id]['lesson_idx'] = 0
    user_data[chat_id]['score'] = 0

    lesson_text = lessons[topic][lang][0]
    bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                          text=f"🎉 {topics[topic][lang]} انتخاب شد!\n\n{texts['lesson_intro'][lang]}\n\n{lesson_text}",
                          reply_markup=next_lesson_markup(0, len(lessons[topic][lang]), lang))

@bot.callback_query_handler(func=lambda call: call.data.startswith('lesson_'))
def lesson_next(call):
    idx = int(call.data.split('_')[1])
    chat_id = call.message.chat.id
    lang = user_data[chat_id]['lang']
    topic = user_data[chat_id]['topic']
    user_data[chat_id]['lesson_idx'] = idx
    lesson_text = lessons[topic][lang][idx]
    bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                          text=f"📚 آموزش شماره {idx+1}:\n\n{lesson_text}",
                          reply_markup=next_lesson_markup(idx, len(lessons[topic][lang]), lang))

@bot.callback_query_handler(func=lambda call: call.data == 'start_questions')
def start_questions(call):
    chat_id = call.message.chat.id
    lang = user_data[chat_id]['lang']
    topic = user_data[chat_id]['topic']
    user_data[chat_id]['question_idx'] = 0
    user_data[chat_id]['score'] = 0

    q_idx = 0
    q, answers, _ = questions[topic][lang][q_idx]
    bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                          text=f"{texts['question_intro'][lang]}\n\nسوال ۱:\n{q}",
                          reply_markup=question_markup(q_idx, answers))

@bot.callback_query_handler(func=lambda call: call.data.startswith('answer_'))
def answer_question(call):
    data = call.data.split('_')
    q_idx = int(data[1])
    ans_idx = int(data[2])
    chat_id = call.message.chat.id
    lang = user_data[chat_id]['lang']
    topic = user_data[chat_id]['topic']

    correct_ans = questions[topic][lang][q_idx][2]

    if ans_idx == correct_ans:
        user_data[chat_id]['score'] += 1
        bot.answer_callback_query(call.id, "👍 درست زدی، عالییی! 🎉")
    else:
        bot.answer_callback_query(call.id, "🙈 اوووه، اشتباه شد!
