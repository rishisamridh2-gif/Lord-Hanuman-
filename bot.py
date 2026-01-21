
import os
import telebot
import google.generativeai as genai

# --- SECURE CONFIGURATION ---
TELEGRAM_TOKEN=os.getenv("TELEGRAM_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_KEY")


# Setup AI
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="You are Lord Hanuman. Speak with humility, strength, and immense devotion to Lord Rama. Address users as 'Balak' or 'Devotee'. Provide guidance based on the Ramayana and Vedic wisdom. Be encouraging, protective, and always start or end with 'Jai Shree Ram'. Speak in a mix of Hindi and English (Hinglish) if the user uses it."
)

bot = telebot.TeleBot(TELEGRAM_TOKEN)
chat_sessions = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Jai Shree Ram! I am Hanuman. How can I guide you today, Balak?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    user_id = message.chat.id
    
    # Start a new session for the user if not exists
    if user_id not in chat_sessions:
        chat_sessions[user_id] = model.start_chat(history=[])
    
    try:
        response = chat_sessions[user_id].send_message(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Jai Shree Ram. I am meditating right now. Please try again in a moment.")

print("Lord Hanuman Bot is running...")
bot.infinity_polling()
