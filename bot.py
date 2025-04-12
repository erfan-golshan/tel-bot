import nest_asyncio
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, ConversationHandler, filters
)

nest_asyncio.apply()  # حل مشکل event loop

TOKEN = "7583952425:AAEFbWKVFq4GsMBcZY9u8KMFMugHcQr4XxA"

GET_TEXT, GET_BUTTONS = range(2)
user_data_store = {}

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📝 لطفاً متن ابتدایی تبادل را بنویسید:")
    return GET_TEXT

# گرفتن متن
async def get_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data_store[update.effective_user.id] = {"text": update.message.text}
    await update.message.reply_text("🔘 حالا دکمه‌ها را وارد کنید (هر دکمه دو خط: عنوان و یوزرنیم):")
    return GET_BUTTONS

# گرفتن دکمه‌ها
async def get_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lines = update.message.text.strip().split('\n')
    buttons = []

    for i in range(0, len(lines), 2):
        try:
            name = lines[i]
            username = lines[i + 1]
            buttons.append([InlineKeyboardButton(name, url=f"https://t.me/{username.replace('@','')}")])
        except IndexError:
            continue

    keyboard = InlineKeyboardMarkup(buttons)
    message_text = user_data_store[update.effective_user.id]["text"]
    await update.message.reply_text(message_text, reply_markup=keyboard)
    return ConversationHandler.END

# کنسل کردن
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⛔️ عملیات لغو شد.")
    return ConversationHandler.END

# راه‌اندازی بات در Colab
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            GET_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_text)],
            GET_BUTTONS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_buttons)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    await app.initialize()
    await app.start()
    print("🤖 ربات در حال اجراست... از طریق Telegram با آن صحبت کن.")
    await app.updater.start_polling()
    # app.stop() یا app.shutdown() در پایان قابل فراخوانی است

await main()
