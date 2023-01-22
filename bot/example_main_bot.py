from API import *

import logging
from typing import Dict

from os import getenv
from time import sleep

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove,  Update, InputMediaPhoto
from telegram.constants import ParseMode
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


TELEGRAM_BOT_TOKEN = getenv("TELEGRAM_API_TOKEN")
if not TELEGRAM_API_TOKEN:
    exit("Please, specify the token env variable!")


def facts_to_str(user_data: Dict[str, str]) -> str:
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "Hi! I can send you lots of photos by your tag.\n"
        "Just type it after this message: no commands needed!\n"
        "For example: ""boobs""."
    )

    return TAG


async def tag(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tag = update.message.text.lower()
    user = update.message.from_user

    logger.info("Tag of %s: %s", user.first_name, update.message.text)

    context.user_data["tag"] = tag

    await update.message.reply_text(
        "Great, now tell me how many photos do you want."
    )

    return QUANTITY


async def quantity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [["Next"]]
    user_data = context.user_data
    user = update.message.from_user

    quantity = update.message.text
    user_data["quantity"] = quantity
    
    logger.info("Quantity of %s: %s", user.first_name, update.message.text)    

    await update.message.reply_text(
        f"Great, so {facts_to_str(user_data)}",
        reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )

    return PHOTO


async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    reply_keyboard = [["Show", "Cancel"]]
    tag = user_data["tag"]
    quantity = user_data["quantity"]
    rq = Rule34(APIBaseUrl, quantity, tag)
    user_data["urls"] = rq.request()
    await update.message.reply_text(
        f"I've been able to get {len(user_data['urls'])} photos with this tag.",
        reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)    
        )
    return SHOW_PHOTO


async def show_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    urls = context.user_data["urls"]
    media_group = []

    for url in urls:
        media = InputMediaPhoto(url)
        media_group.append(media)

    try:
        await update.message.reply_media_group(media = media_group)
    except:
        start = 0
        end = len(media_group)
        step = 10
        for i in range(start, end, step):
            x = i
            await update.message.reply_media_group(media = media_group[x:x+step])
            sleep(2)

    await update.message.reply_text(
        "That's it! If you want to start over just type /start.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


async def tag_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    message = (
       "There is no such tag! Try again: /start."
    )
    await context.bot.send_message(
        chat_id = update.effective_chat.id, text=message, parse_mode=ParseMode.HTML
    )


#async def limit_error(update: object, context: ContextTypes.DEFAULT_TYPE):
    


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await update.message.reply_text(
        f"Okay, bye."
    )
    return ConversationHandler.END


def main():

    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states = {
            TAG: [MessageHandler(filters.TEXT, tag)],
            QUANTITY: [MessageHandler(filters.TEXT, quantity)],
            PHOTO: [MessageHandler(filters.TEXT, photo)],
            SHOW_PHOTO: [
                MessageHandler(filters.Regex("^(Show)$"), show_photo)]
        },
        fallbacks=[MessageHandler(filters.Regex("^(Done|No|Cancel)$"), done)],
    )
    
    application.add_handler(conv_handler)
    application.add_error_handler(tag_error)
    application.run_polling(timeout=600)


if __name__ == "__main__":
    main()    