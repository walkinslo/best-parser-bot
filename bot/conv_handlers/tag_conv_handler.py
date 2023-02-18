import logging
from API import *
from message_texts import *
from config import TAG_ELEMENTS_COUNT
from services.message_to_tag import message_to_tag
from services.photos import send_photos

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove,  Update, InputMediaPhoto
from telegram.ext import ContextTypes, ConversationHandler
from telegram.constants import ParseMode


TAG, SHOW_PHOTO = range(2)

logging.basicConfig(
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level = logging.INFO
)
logger = logging.getLogger(__name__)

async def tag(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [["Show", "Cancel"]]
    message = update.message.text.lower()
    
    tag_from_message = message_to_tag(message)
    if not _is_numbers_sufficient(tag_from_message):
        await update.message.reply_text(text = TAG_INVALID_INPUT)
        return

    tag = tag_from_message[0]
    quantity = tag_from_message[1]

    user_data = context.user_data

    rq = Rule34(APIBaseUrl, quantity, tag)
    user_data["urls"] = rq.request()

    if len(user_data["urls"]) == 0:
        await update.message.reply_text(text = NO_TAG_ERROR)
        return

    await update.message.reply_text(
        f"I've been able to get {len(user_data['urls'])} photos with this tag.",
        reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)    
        )

    return SHOW_PHOTO


async def show_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await send_photos(update, context)

    return ConversationHandler.END

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await update.message.reply_text(
        f"Okay, bye. If you change your mind - send me /tag :)",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def _is_numbers_sufficient(numbers: list[int]) -> bool:
    return len(numbers) == TAG_ELEMENTS_COUNT

