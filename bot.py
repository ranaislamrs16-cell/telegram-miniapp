
import asyncio
import logging
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from google import genai

# Render-এর পোর্ট সন্তুষ্ট করার জন্য অত্যন্ত হালকা একটি লোকাল সার্ভার
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"RS AI Support Bot is active and running!")

def run_http_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

# জেমিনি এবং টেলিগ্রাম কনফিগারেশন
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
        if response and response.text:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("দুঃখিত, এই মুহূর্তে কোনো উত্তর পাওয়া যায়নি।")
    except Exception as e:
        print(f"AI Error: {e}")
        await update.message.reply_text("দুঃখিত, এই মুহূর্তে উত্তর দিতে সমস্যা হচ্ছে। একটু পর আবার চেষ্টা করুন।")

async def main():
    # ব্যাকগ্রাউন্ডে ছোট HTTP সার্ভার চালু করা যা Render-এর পোর্ট চাহিদা পূরণ করবে
    server_thread = Thread(target=run_http_server, daemon=True)
    server_thread.start()

    # টেলিগ্রাম বটের কাজ
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
