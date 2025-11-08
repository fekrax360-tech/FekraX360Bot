import telebot
import openai
import os

# Telegram bot token and OpenAI key
BOT_TOKEN = os.getenv("TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "👋 أهلاً بك في بوت فكرة X360! أرسل برومبت لتوليد صورة واقعية.")

@bot.message_handler(func=lambda message: True)
def generate_image(message):
    try:
        prompt = message.text
        bot.reply_to(message, "⏳ جاري توليد الصورة، يرجى الانتظار...")

        result = openai.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024"
        )

        image_url = result.data[0].url
        bot.send_photo(message.chat.id, image_url, caption="✅ تم الإنشاء بواسطة FekraX360 | AI Vision")

    except Exception as e:
        bot.reply_to(message, f"⚠️ حدث خطأ أثناء المعالجة:\n{e}")

if __name__ == "__main__":
    print("🤖 Bot is running...")
    bot.polling(none_stop=True)
