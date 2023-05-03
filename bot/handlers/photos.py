from telegram import Update
from telegram.ext import ContextTypes

from .keyboards import get_photos_keyboard
from .response import send_message


async def send_photos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_chat = update.effective_chat
    urls = context.user_data["urls"]
    photos_count = len(urls)

    try:
        await context.bot.send_photo(
            photo=urls[0],
            chat_id=effective_chat.id,
            reply_markup=get_photos_keyboard(0, photos_count)
        )
    except Exception:
        await send_message(
            update,
            context,
            response="Oops! It appears that the image that I wanted to send was unsupported by telegram"
        )
        await send_message(
            update,
            context,
            response=f"Here is the link in case you want to see it: {urls[0]}"
        )
        del urls[0]
        await context.bot.send_photo(
            photo=urls[0],
            chat_id=effective_chat.id,
            reply_markup=get_photos_keyboard(0, photos_count)
        )
