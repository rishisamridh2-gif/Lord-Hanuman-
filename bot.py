import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread

# --- WEB SERVER FOR RENDER ---
app = Flask('')
@app.route('/')
def home():
    return "Lord Hanuman Bot is Alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

# --- BOT LOGIC ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
API_KEY = os.getenv("GEMINI_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Jai Shree Ram! Main Hanuman hoon. Kaise sahayata karoon, Balak?")

@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        response = model.generate_content(f"Act as Lord Hanuman: {message.text}")
        bot.reply_to(message, response.text)
    except:
        bot.reply_to(message, "Jai Shree Ram. Kuch samay baad prayas karein.")

# Start Web Server and Bot
if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    print("Bot is starting...")
    bot.infinity_polling()
