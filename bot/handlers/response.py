import telegram

from telegram import InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes


async def send_message(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        response: str,
        keyboard: InlineKeyboardMarkup | None = None
) -> None:
    args = {
            "text": response,
            "parse_mode": telegram.constants.ParseMode.HTML,
    }
    if keyboard:
        args["reply_markup"] = keyboard
        args["one_time_keyboard"] = True

    await update.message.reply_text(**args)
