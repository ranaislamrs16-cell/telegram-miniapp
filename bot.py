
import asyncio
import logging
import os
from aiohttp import web
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from google import genai

# রেন্ডার সার্ভার সচল রাখার জন্য হালকা ওয়েব সার্ভার
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

# আপনার দেওয়া জেমিনি এপিআই কি এবং টেলিগ্রাম বটের টোকেন এখানে বসানো হলো
client = genai.Client(api_key="AQ.Ab8RN6IyOvW5q5TAtolHlLhdbR4cd7MVv2tCMwP2iXDtJndSMQ")
TELEGRAM_BOT_TOKEN = "8850565414:AAE7iqrTaRma-Lqxfcwe5QxWFeb84MJ5O6E"

# কাস্টমার বা ব্যবহারকারীদের জন্য এআই অ্যাসিস্ট্যান্টের নির্দেশিকা
SYSTEM_INSTRUCTION = """
আপনি RS Tap & Earn মিনি অ্যাপের একজন অফিশিয়াল AI ব্যাকএন্ড সাপোর্ট সহকারী।
আপনার কাজ হলো ব্যবহারকারীদের $RS টোকেন, পয়েন্ট আর্নিং, টাস্ক, ডিপোজিট, উইথড্র এবং অ্যাকাউন্ট সংক্রান্ত যেকোনো প্রশ্নের খুব সুন্দর ও নিখুঁত উত্তর দেওয়া।
সবসময় বিনীত, পেশাদার ও সংক্ষিপ্ত ভাষায় উত্তর দেবেন যাতে কাস্টমার কোনো ধরনের সমস্যায় না পড়ে।
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("স্বাগতম! আমি RS AI সাপোর্ট অ্যাসিস্ট্যান্ট। $RS টোকেন, পয়েন্ট আর্নিং বা অ্যাপ সংক্রান্ত যেকোনো প্রশ্ন করতে পারেন। আপনাকে কীভাবে সাহায্য করতে পারি?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    full_prompt = f"{SYSTEM_INSTRUCTION}\n\nইউজার প্রশ্ন করেছেন: {user_text}\nউত্তর:"
    
    try:
        # জেমিনির সঠিক মডেল ব্যবহার করে এআই রেসপন্স জেনারেট করা হচ্ছে
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=full_prompt,
        )
        if response and response.text:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("দুঃখিত, এই মুহূর্তে কোনো উত্তর পাওয়া যায়নি। একটু পরে আবার চেষ্টা করুন।")
    except Exception as e:
        print(f"AI Error Details: {e}")
        await update.message.reply_text("দুঃখিত, এই মুহূর্তে সার্ভারে একটু সমস্যা হচ্ছে। একটু পর আবার চেষ্টা করুন।")

async def main():
    # ওয়েব সার্ভার এবং টেলিগ্রাম বট একসাথে স্টার্ট করা
    await start_web_server()

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    await app.initialize()
    await app.start()
    app.updater.start_polling()
    
    stop_signal = asyncio.Event()
    await stop_signal.wait()

if __name__ == '__main__':
    asyncio.run(main())
