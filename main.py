

import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
import requests

# --- API TOKENLAR ---
TELEGRAM_TOKEN="7961468443:AAGjSE6173CvN6G2bxLpXEkwFVpUJ-SGK1Y"
GROQ_API_KEY="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"

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! Men siz hohlagan savollaringizga javob beraman va men Xaydarova Dilshoda tomonidan yaratilganman.\n"
        "Savolingizni yozing:"
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # Loader xabarni yuborish
    loader_message = await update.message.reply_text("⏳ Javob o'ylanmoqda...")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": user_text}
        ]
    }

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data
        ).json()

        bot_reply = response["choices"][0]["message"]["content"]
        
        # Loader xabarni o'chirish va javob yuborish
        await loader_message.delete()
        await update.message.reply_text(bot_reply)
    except Exception as e:
        await loader_message.delete()
        await update.message.reply_text(f"❌ Xato yuz berdi: {str(e)}")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    app.run_polling()

if __name__ == "__main__":
    main()