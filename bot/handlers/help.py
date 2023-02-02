from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

import message_texts


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text = message_texts.HELP,
        parse_mode=ParseMode.HTML
        )