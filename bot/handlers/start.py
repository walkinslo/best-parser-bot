from telegram import Update
from telegram.ext import ContextTypes

import bot.message_texts
from bot.handlers.response import send_message


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_message(update, context, response=bot.message_texts.GREETING)
