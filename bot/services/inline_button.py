from telegram import Update
from telegram.ext import ContextTypes

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    await query.answer()

    await query.edit_message_media(text=f"Selected option: {query.data}")