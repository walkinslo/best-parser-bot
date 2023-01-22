from API import *
import message_texts

import logging
from typing import Dict

from os import getenv
from time import sleep

from telegram import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
    InputMediaPhoto
)
from telegram.ext import (
    Application, 
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters
)

logging.basicConfig(
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s", level = logging.INFO
)
logger = logging.getLogger(__name__)


TELEGRAM_API_TOKEN = getenv("TELEGRAM_API_TOKEN")
if not TELEGRAM_API_TOKEN:
    exit("Please, specify the token env variable!")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text = message_texts.GREETING
    )


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text = message_texts.HELP
    )


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()