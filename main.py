import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Read the bot token from the environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN found in environment variables!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your bot.")

def main():
    # Build the application
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add the /start command handler
    app.add_handler(CommandHandler("start", start))

    # Start the bot in polling mode
    print("Starting bot in polling mode...")
    app.run_polling()

if __name__ == "__main__":
    main()