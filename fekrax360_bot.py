import os, io, base64, telebot, requests

TOKEN = os.getenv("TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TOKEN:
    raise RuntimeError("TOKEN is missing.")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "جاهز ✅\nاكتب /generate_news_photo للبدء.")

@bot.message_handler(commands=['generate_news_photo'])
def ask_name(m):
    bot.reply_to(m, "📸 أرسل اسم الشخص (يمكن أن يكون رمزي/خيالي):")
    bot.register_next_step_handler(m, ask_expression)

def ask_expression(m):
    global person_name
    person_name = m.text.strip()
    bot.reply_to(m, "🙂 أرسل ملامح الوجه (angry, sad, confident …):")
    bot.register_next_step_handler(m, ask_background)

def ask_background(m):
    global expression
    expression = m.text.strip()
    bot.reply_to(m, "🌆 أرسل الخلفية (newsroom, destroyed buildings …):")
    bot.register_next_step_handler(m, generate_image)

def generate_image(m):
    background = m.text.strip()
    prompt = f"""
Create a realistic, high-quality news-style portrait featuring {person_name} as the main subject.
Show the person from the chest up, facing the camera, with a {expression} expression.
Lighting should be cinematic and balanced, focused mainly on the face.
In the background, add a {background}, softly blurred and thematically connected to the subject.
Use FekraX360 visual identity — deep blue gradient base, cool cyan highlights, smooth shadows.
At the bottom, include the FekraX360 | News logo strip with a golden Palestine map emblem.
Keep precise facial detail and a polished newsroom look, suitable for Telegram posts.
""".strip()

    if not OPENAI_API_KEY:
        bot.send_message(m.chat.id, "❌ لا يوجد OPENAI_API_KEY في إعدادات Render.")
        return

    bot.send_message(m.chat.id, "⏳ جاري توليد الصورة عبر DALL·E…")

    try:
        # استدعاء واجهة توليد الصور (gpt-image-1)
        resp = requests.post(
            "https://api.openai.com/v1/images/generations",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-image-1",
                "prompt": prompt,
                "size": "1024x1024",
                "n": 1
            },
            timeout=180
        )
        if resp.status_code != 200:
            bot.send_message(m.chat.id, f"❌ فشل التوليد ({resp.status_code}): {resp.text[:200]}")
            return

        data = resp.json()
        b64 = data["data"][0].get("b64_json")
        if not b64:
            bot.send_message(m.chat.id, "❌ لم يتم استلام بيانات الصورة من واجهة OpenAI.")
            return

        img_bytes = base64.b64decode(b64)
        with io.BytesIO(img_bytes) as buf:
            buf.name = "image.png"
            bot.send_photo(m.chat.id, buf, caption="✅ الصورة الجاهزة | FekraX360")

    except Exception as e:
        bot.send_message(m.chat.id, f"❌ خطأ غير متوقع: {e}")

bot.infinity_polling(skip_pending=True)
