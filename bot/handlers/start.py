from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

import message_texts

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text = message_texts.GREETING,
        parse_mode=ParseMode.HTML
        )