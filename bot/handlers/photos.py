from telegram import (
        Update, 
        InlineKeyboardButton, 
        InlineKeyboardMarkup, 
        InputMediaPhoto
)
from telegram.ext import ContextTypes
    
def _get_photos_keyboard(current_index: int) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(" < ", callback_data=current_index - 1),
            InlineKeyboardButton(" > ", callback_data=current_index + 1),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


async def send_photos(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
