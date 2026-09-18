
import asyncio
import logging
import os
from aiohttp import web
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from google import genai

# ফ্রিতে রেন্ডারকে খুশি রাখার জন্য aiohttp দিয়ে একটি হালকা ওয়েব সার্ভার
async def handle_web(request):
    return web.Response(text="RS AI Support Bot is running live!")

async def start_web_server():
    app_web = web.Application()
    app_web.router.add_get("/", handle_web)
    runner = web.AppRunner(app_web)
    await runner.setup()
    
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

# জেমিনি এবং টেলিগ্রাম কনফিগারেশন
# (আপনার দেওয়া এপিআই কি অপরিবর্তিত রাখা হয়েছে)
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
        # জেমিনির সঠিক মডেল নেম দিয়ে এপিআই কল করা হচ্ছে
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=full_prompt,
        )
        if response and response.text:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("দুঃখিত, এই মুহূর্তে কোনো উত্তর পাওয়া যায়নি।")
    except Exception as e:
        # রেন্ডার লগে আসল এরর প্রিন্ট করার ব্যবস্থা, যাতে ভবিষ্যতে ধরতে সুবিধা হয়
        print(f"AI Error Details: {e}")
        await update.message.reply_text(f"দুঃখিত, টেকনিক্যাল সমস্যার কারণে উত্তর দিতে পারছি না।")

async def main():
    await start_web_server()

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    
    stop_signal = asyncio.Event()
    await stop_signal.wait()

if __name__ == '__main__':
    asyncio.run(main())
