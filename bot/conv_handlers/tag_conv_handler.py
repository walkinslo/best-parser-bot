from API import *
from typing import Dict
from time import sleep

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove,  Update, InputMediaPhoto

from telegram.ext import ContextTypes, ConversationHandler


TAG, QUANTITY, PHOTO, SHOW_PHOTO = range(4)


def facts_to_str(user_data: Dict[str, str]) -> str:
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])


async def tag_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tag = update.message.text.lower()

    context.user_data["tag"] = tag

    await update.message.reply_text(
        "Great, now tell me how many photos do you want."
    )

    return QUANTITY


async def quantity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [["Next"]]
    user_data = context.user_data

    quantity = update.message.text
    user_data["quantity"] = quantity
    

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
        "That's it! If you want to start over just type /tag.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await update.message.reply_text(
        f"Okay, bye."
    )
    return ConversationHandler.END




