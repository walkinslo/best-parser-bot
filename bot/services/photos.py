import logging

from collections import Counter

from telegram import Update, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ContextTypes, CallbackQueryHandler

from .helpers import append_into_media_group


async def send_photos(update: Update, context: ContextTypes.DEFAULT_TYPE):

    urls = context.user_data["urls"]

    media_group = append_into_media_group(urls)

    try:
        await update.message.reply_media_group(media = media_group)
    except Exception:
        import traceback

        logging.warning(traceback.format_exc())

        start = 0
        end = len(media_group)
        step = 10
        
        for i in range(start, end, step):
            x = i
            await update.message.reply_media_group(media = media_group[x:x+step])
    
    await update.message.reply_text(
        "That's it! If you want to start over just type /tag.",
        reply_markup=ReplyKeyboardRemove()
    )
    

def _get_photos_keyboard(current_index: int) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data=current_index - 1),
            InlineKeyboardButton("Option 2", callback_data=current_index + 1),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


async def tmp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_chat = update.effective_chat

    urls = context.user_data["urls"]

    try: 
        await context.bot.send_photo(
            photo=urls[0], 
            chat_id=effective_chat.id, 
            reply_markup=_get_photos_keyboard(0)
        )
    except Exception:
        del urls[0]
        await context.bot.send_photo(
            photo=urls[0], 
            chat_id=effective_chat.id, 
            reply_markup=_get_photos_keyboard(0)
        )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    urls = context.user_data["urls"]
    current_index = int(query.data)

    await query.edit_message_media(
        media = InputMediaPhoto(urls[current_index]),
        reply_markup = _get_photos_keyboard(current_index)
    )