import logging

from telegram import Update, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ContextTypes, CallbackQueryHandler

from .helpers import append_into_media_group
from .keyboards import get_photos_keyboard

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
    

async def tmp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_chat = update.effective_chat
    urls = context.user_data["urls"]
    current_photo_index = int(query.data)
    photos_count = len(urls)

    try: 
        await context.bot.send_photo(
            photo=urls[0], 
            chat_id=effective_chat.id, 
            reply_markup=get_photos_keyboard(photos_count=photos_count, current_photo_index=current_photo_index)
        )
    except Exception:
        del urls[0]
        await context.bot.send_photo(
            photo=urls[0], 
            chat_id=effective_chat.id,  
            reply_markup=get_photos_keyboard(photos_count=photos_count, current_photo_index=current_photo_index)
        )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    urls = context.user_data["urls"]
    current_index = int(query.data)

    await query.edit_message_media(
        media = InputMediaPhoto(urls[current_index]),
        reply_markup = get_photos_keyboard(photos_count=len(urls), current_photo_index=current_index)
    )
