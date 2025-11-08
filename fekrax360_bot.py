import os, telebot

# قراءة التوكن من متغير البيئة
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("⚠️ TOKEN غير موجود! أضف متغير البيئة TOKEN قبل التشغيل.")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "👋 مرحباً! اكتب /generate_news_photo للبدء.")

@bot.message_handler(commands=['generate_news_photo'])
def ask_name(m):
    bot.reply_to(m, "📸 أرسل اسم الشخص:")
    bot.register_next_step_handler(m, ask_expression)

def ask_expression(m):
    global person_name
    person_name = m.text.strip()
    bot.reply_to(m, "🙂 أرسل ملامح الوجه (angry, sad, confident...):")
    bot.register_next_step_handler(m, ask_background)

def ask_background(m):
    global expression
    expression = m.text.strip()
    bot.reply_to(m, "🌆 أرسل نوع الخلفية (newsroom, destroyed buildings, angry Netanyahu...):")
    bot.register_next_step_handler(m, generate_image)

def generate_image(m):
    background = m.text.strip()
    prompt = f"""
Create a realistic, high-quality news-style portrait featuring {person_name} as the main subject.
Show the person from the chest up, facing the camera, with a {expression} expression.
Lighting should be cinematic and balanced, focused mainly on the face.
In the background, add a {background}, softly blurred and thematically connected to the subject.
The overall tone must remain consistent with FekraX360’s visual identity — deep blue gradient base, cool cyan highlights, and smooth shadows.
At the bottom, include the FekraX360 | News logo and the golden Palestine map emblem with social media icons in a clean strip.
Maintain precise facial detail and a polished newsroom look.
    """.strip()

    bot.send_message(m.chat.id, "⏳ يتم تجهيز البرومبت...")
    bot.send_message(m.chat.id, f"✅ البرومبت الجاهز:\n\n{prompt}")

bot.infinity_polling(skip_pending=True)
