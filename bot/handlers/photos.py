from telegram import (
        Update, 
        ReplyKeyboardRemove
)
from telegram.ext import ContextTypes

from .keyboards import get_photos_keyboard


async def send_photos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_chat = update.effective_chat

    urls = context.user_data["urls"]
    
    photos_count = len(urls)

    if photos_count == 0:
        await context.bot.send_photo(
                photo = urls[0],
                chat_id = effective_chat,
                reply_markup = ReplyKeyboardRemove()
        )

    try: 
        await context.bot.send_photo(
            photo=urls[0], 
            chat_id = effective_chat.id, 
            reply_markup = get_photos_keyboard(0, photos_count)
        )
    except Exception:
        del urls[0]
        await context.bot.send_photo(
            photo = urls[0], 
            chat_id = effective_chat.id, 
            reply_markup = get_photos_keyboard(0, photos_count)
        )
