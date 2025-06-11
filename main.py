from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

# === CONFIGURATION ===
BOT_TOKEN = "7552725572:AAFxjg1TbQlK8QgRmlAWFAOTBvkfRmEsq7I"
ADMIN_USER_ID = 1749445258 # Replace with your Telegram ID

# === Detection Settings ===
BANNED_KEYWORDS = ["coupon", "promo", "code", "discount", "use"]
recent_messages = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is running!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    user_id = update.message.from_user.id
    text = update.message.text.lower()

    if user_id == ADMIN_USER_ID:
        return

    if any(word in text for word in BANNED_KEYWORDS):
        await update.message.delete()
        return

    if recent_messages.get(user_id) == text:
        await update.message.delete()
        return

    recent_messages[user_id] = text

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
