import asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from google import genai

client = genai.Client(api_key="AQ.Ab8RN6LAY2E20xSQ4w_RfvgKyrmZ6UXZewMMRnnTJHvmI-PATA")
TELEGRAM_BOT_TOKEN = "8850565414:AAE7iqrTaRma-Lqxfcwe5QxWFeb84MJ5O6E"

SYSTEM_INSTRUCTION = """
আপনি RS Tap & Earn মিনি অ্যাপের একজন অফিশিয়াল AI ব্যাকএন্ড সাপোর্ট সহকারী।
আপনার কাজ হলো ব্যবহারকারীদের $RS টোকেন, পয়েন্ট আর্নিং, টাস্ক এবং অ্যাকাউন্ট সংক্রান্ত প্রশ্নের উত্তর দেওয়া।
সবসময় বিনীত ও সংক্ষিপ্ত ভাষায় উত্তর দেবেন।
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("স্বাগতম! আমি RS AI সাপোর্ট অ্যাসিস্ট্যান্ট। $RS টোকেন বা অ্যাপ সংক্রান্ত যেকোনো প্রশ্ন করতে পারেন।")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    full_prompt = f"{SYSTEM_INSTRUCTION}\n\nইউজার প্রশ্ন করেছেন: {user_text}\nউত্তর:"
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=full_prompt,
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("দুঃখিত, এই মুহূর্তে উত্তর দিতে সমস্যা হচ্ছে। একটু পর আবার চেষ্টা করুন।")

async def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    # Render-এর লেটেস্ট পাইথনের জন্য নিরাপদ এসিনক্রোনাস স্টার্টিং
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    
    # বট যেন বন্ধ না হয়ে সচল থাকে
    stop_signal = asyncio.Event()
    await stop_signal.wait()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except RuntimeError:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
