import logging

from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes

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