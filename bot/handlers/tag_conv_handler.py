import logging

import message_texts
from .response import send_message
from .photos import send_photos
from services.API import APIBaseUrl, Rule34 
from services.helpers import _is_numbers_sufficient, message_to_tag

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler


TAG, SHOW_PHOTO = range(2)


logging.basicConfig(
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level = logging.INFO
)
logger = logging.getLogger(__name__)


async def tag(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [["Show", "Cancel"]]
    message = update.message.text.lower()
    user_data = context.user_data

    tag_from_message = message_to_tag(message)

    if not _is_numbers_sufficient(tag_from_message):
        await send_message(
                update,
                context, 
                response = message_texts.TAG_INVALID_INPUT
        )
        return
    

    quantity = tag_from_message[1]
    tag = tag_from_message[0]

    rq = Rule34(APIBaseUrl, quantity, tag)
    user_data["urls"] = rq.request()
    photos_count = len(user_data["urls"])

    if photos_count == 0:
        await send_message(
                update, 
                context, 
                reponse = message_texts.NO_TAG_ERROR
        )
        return

    await update.message.reply_text(
            f"I've been able to get {photos_count} photos with this tag.",
            reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)    
        )

    return SHOW_PHOTO


async def show_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await send_photos(update, context)
    
    await send_message(
            update, 
            context,
            response = message_texts.DONE
    )

    return ConversationHandler.END


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    await send_message(
            update,
            context,
            response = message_texts.DONE 
    )

    return ConversationHandler.END


