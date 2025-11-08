import telebot
import requests
import os

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# استخدم OpenAI أو أي API لتوليد الصور (هنا سنستخدم واجهة DALL-E عبر Render مثلاً)
# لكن لتبسيط الشرح سنستخدم رابط توليد صور افتراضي كمثال

def generate_image(prompt):
    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/prompthero/openjourney",
            headers={"Authorization": "Bearer hf_your_api_key"},
            json={"inputs": prompt}
        )
        image_bytes = response.content
        file_path = "generated_image.jpg"
        with open(file_path, "wb") as f:
            f.write(image_bytes)
        return file_path
    except Exception as e:
        print("Error generating image:", e)
        return None

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    prompt = message.text
    bot.send_message(message.chat.id, "⏳ جاري توليد الصورة...")
    image_path = generate_image(prompt)
    if image_path:
        with open(image_path, "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption="✅ تم توليد الصورة بواسطة FekraX360")
        os.remove(image_path)
    else:
        bot.send_message(message.chat.id, "❌ حدث خطأ أثناء توليد الصورة. حاول مجددًا.")

bot.polling(none_stop=True)
