import message_texts
from conv_handlers.tag_conv_handler import (
   tag_handler,
   quantity,
   photo,
   show_photo,
   done
)

import logging

from os import getenv

from telegram import Update
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


TAG, QUANTITY, PHOTO, SHOW_PHOTO = range(4)


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


async def tag(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        text = message_texts.TAG
    )

    return TAG


def main() -> None:
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    tag_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("tag", tag)],
        states = {
            TAG: [MessageHandler(filters.TEXT, tag_handler)],
            QUANTITY: [MessageHandler(filters.TEXT, quantity)],
            PHOTO: [MessageHandler(filters.TEXT, photo)],
            SHOW_PHOTO: [MessageHandler(filters.Regex("^(Show)$"), show_photo)]
        },
        fallbacks=[MessageHandler(filters.Regex("^(Done|No|Cancel)$"), done)],
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))

    application.add_handler(tag_conv_handler)

    application.run_polling()


if __name__ == "__main__":
    main()