import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import aiohttp

API_TOKEN = "7898327343:AAHfKAfWghG7c8Kn8DDSz3ouWdbblLx7_QY"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

LANGUAGES = {"fa": "فارسی", "en": "English", "ar": "العربية"}

user_lang = {}
user_state = {}  # نگهداری حالت هر کاربر: None یا "translate" یا "weather" یا "calc" یا "reminder"

main_menu_buttons = {
    "fa": ["ترجمه متن", "اخبار", "آب و هوا", "ماشین حساب", "جوک", "یادآوری"],
    "en": ["Translate Text", "News", "Weather", "Calculator", "Joke", "Reminder"],
    "ar": ["ترجمة النص", "الأخبار", "الطقس", "آلة حاسبة", "نكتة", "تذكير"]
}

async def translate_text(text, target_lang):
    url = "https://api.mymemory.translated.net/get"
    params = {"q": text, "langpair": f"auto|{target_lang}"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            data = await resp.json()
            try:
                return data["responseData"]["translatedText"]
            except:
                return "Error in translation"

async def get_news(lang):
    news = {
        "fa": "خبر: امروز هوا آفتابی است.",
        "en": "News: Today the weather is sunny.",
        "ar": "خبر: الطقس مشمس اليوم."
    }
    return news.get(lang, news["en"])

async def get_weather(city, lang):
    responses = {
        "fa": f"آب و هوای شهر {city} امروز آفتابی و ۳۰ درجه است.",
        "en": f"Weather in {city} today is sunny and 30°C.",
        "ar": f"الطقس في {city} اليوم مشمس و 30 درجة."
    }
    return responses.get(lang, responses["en"])

async def get_joke(lang):
    jokes = {
        "fa": "یه مرد به دکتر گفت: دکتر جان، هر بار قهوه می‌خورم چشمم درد می‌گیره! دکتر گفت: قاشق رو از لیوان بیرون بیار!",
        "en": "Why don’t scientists trust atoms? Because they make up everything!",
        "ar": "لماذا لا يثق العلماء بالذرات؟ لأنها تكون كل شيء!"
    }
    return jokes.get(lang, jokes["en"])

def get_language_code_by_name(name):
    for code, lang_name in LANGUAGES.items():
        if name == lang_name:
            return code
    return None

def create_main_menu_keyboard(lang):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for btn in main_menu_buttons[lang]:
        kb.add(KeyboardButton(btn))
    return kb

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for name in LANGUAGES.values():
        kb.add(KeyboardButton(name))
    await message.answer(
        "لطفا زبان خود را انتخاب کنید\nPlease choose your language\nيرجى اختيار لغتك",
        reply_markup=kb
    )
    user_state[message.from_user.id] = None
    user_lang.pop(message.from_user.id, None)

@dp.message_handler()
async def handle_all_messages(message: types.Message):
    user_id = message.from_user.id
    text = message.text

    # اگر زبان انتخاب نشده، سعی کن انتخاب زبان رو پیدا کنی
    if user_id not in user_lang:
        lang_code = get_language_code_by_name(text)
        if lang_code:
            user_lang[user_id] = lang_code
            user_state[user_id] = None
            kb = create_main_menu_keyboard(lang_code)
            await message.answer({"fa": "منوی اصلی:", "en": "Main Menu:", "ar": "القائمة الرئيسية:"}[lang_code], reply_markup=kb)
        else:
            kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            for name in LANGUAGES.values():
                kb.add(KeyboardButton(name))
            await message.answer(
                "لطفا زبان خود را انتخاب کنید\nPlease choose your language\nيرجى اختيار لغتك",
                reply_markup=kb
            )
        return

    lang = user_lang[user_id]

    # اگر در حالت خاصی هستیم، پیام کاربر بر اساس حالت بررسی شود
    state = user_state.get(user_id)

    if state == "translate":
        translated = await translate_text(text, lang)
        await message.answer(translated)
        user_state[user_id] = None
        kb = create_main_menu_keyboard(lang)
        await message.answer({"fa": "منوی اصلی:", "en": "Main Menu:", "ar": "القائمة الرئيسية:"}[lang], reply_markup=kb)
        return

    elif state == "weather":
        weather = await get_weather(text, lang)
        await message.answer(weather)
        user_state[user_id] = None
        kb = create_main_menu_keyboard(lang)
        await message.answer({"fa": "منوی اصلی:", "en": "Main Menu:", "ar": "القائمة الرئيسية:"}[lang], reply_markup=kb)
        return

    elif state == "calc":
        try:
            allowed_chars = "0123456789+-*/(). "
            if any(ch not in allowed_chars for ch in text):
                raise ValueError
            result = eval(text)
            await message.answer(str(result))
        except:
            await message.answer({"fa": "فرمول نامعتبر است", "en": "Invalid formula", "ar": "صيغة غير صالحة"}[lang])
        user_state[user_id] = None
        kb = create_main_menu_keyboard(lang)
        await message.answer({"fa": "منوی اصلی:", "en": "Main Menu:", "ar": "القائمة الرئيسية:"}[lang], reply_markup=kb)
        return

    elif state == "reminder":
        try:
            minutes = int(text)
            await message.answer({"fa": f"یادآوری در {minutes} دقیقه فعال شد", "en": f"Reminder set for {minutes} minutes", "ar": f"تم ضبط التذكير بعد {minutes} دقيقة"}[lang])
            # اجرای یادآوری به صورت غیرهمزمان (این تابع پاسخ سریع می‌دهد و بعد یادآوری را ارسال می‌کند)
            asyncio.create_task(reminder_task(user_id, minutes, lang))
        except:
            await message.answer({"fa": "عدد معتبر وارد کنید", "en": "Enter a valid number", "ar": "أدخل رقما صحيحا"}[lang])
        user_state[user_id] = None
        kb = create_main_menu_keyboard(lang)
        await message.answer({"fa": "منوی اصلی:", "en": "Main Menu:", "ar": "القائمة الرئيسية:"}[lang], reply_markup=kb)
        return

    # اگر حالت خاصی نیست، پیام کاربر بررسی می‌شود (منوی اصلی)
    if text == main_menu_buttons[lang][0]:  # ترجمه متن
        user_state[user_id] = "translate"
        await message.answer({"fa": "لطفا متن را ارسال کنید:", "en": "Please send the text:", "ar": "يرجى إرسال النص:"}[lang])
    elif text == main_menu_buttons[lang][1]:  # اخبار
        news = await get_news(lang)
        await message.answer(news)
    elif text == main_menu_buttons[lang][2]:  # آب و هوا
        user_state[user_id] = "weather"
        await message.answer({"fa": "نام شهر را بفرستید:", "en": "Send city name:", "ar": "أرسل اسم المدينة:"}[lang])
    elif text == main_menu_buttons[lang][3]:  # ماشین حساب
        user_state[user_id] = "calc"
        await message.answer({"fa": "فرمول محاسبه را به صورت ساده وارد کنید (مثال: 2+2):", "en": "Enter calculation formula (example: 2+2):", "ar": "أدخل صيغة الحساب (مثال: 2+2):"}[lang])
    elif text == main_menu_buttons[lang][4]:  # جوک
        joke = await get_joke(lang)
        await message.answer(joke)
    elif text == main_menu_buttons[lang][5]:  # یادآوری
        user_state[user_id] = "reminder"
        await message.answer({"fa": "زمان یادآوری را به دقیقه وارد کنید:", "en": "Enter reminder time in minutes:", "ar": "أدخل وقت التذكير بالدقائق:"}[lang])
    else:
        kb = create_main_menu_keyboard(lang)
        await message.answer({"fa": "لطفا یکی از گزینه‌های منو را انتخاب کنید.", "en": "Please select an option from the menu.", "ar": "يرجى اختيار خيار من القائمة."}[lang], reply_markup=kb)

async def reminder_task(user_id, minutes, lang):
    await asyncio.sleep(minutes * 60)
    try:
        await bot.send_message(user_id, {"fa": "یادآوری شما! ⏰", "en": "Your reminder! ⏰", "ar": "تذكيرك! ⏰"}[lang])
    except:
        pass

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
