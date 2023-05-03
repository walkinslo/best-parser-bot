from telegram import (
    Update,
    InputMediaPhoto
)
from telegram.ext import ContextTypes

from .photos import get_photos_keyboard

TAG = 0

async def pagination_button(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> int:
    query = update.callback_query
    await query.answer()

    urls = context.user_data["urls"]
    photos_count = len(urls)
    try:
        current_index = int(query.data)
        await query.edit_message_media(
            media=InputMediaPhoto(urls[current_index]),
            reply_markup=get_photos_keyboard(current_index, photos_count)
        )
    except ValueError:
        context.user_data.clear()
        return TAG
