from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.environ.get("GROQ_API_KEY")
TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من فندوقم 🐰 هر سوالی داری بپرس!")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    await update.message.reply_text("داری فکر می‌کنم... 🐰")
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:5000",
                "X-Title": "Fandogh AI"
            },
            json={
                "model": "mistralai/mistral-7b-instruct:free",
                "messages": [{"role": "user", "content": user_msg}]
            }
        )
        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)
        result = response.json()
        reply = result["choices"][0]["message"]["content"]
        await update.message.reply_text(reply)
    except Exception as e:
        print("ERROR:", e)
        await update.message.reply_text("خطا پیش اومد، دوباره امتحان کن 🐰")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
app.run_polling()
