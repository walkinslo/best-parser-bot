from telegram import Update
from telegram.ext import ContextTypes

import message_texts


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text = message_texts.HELP)