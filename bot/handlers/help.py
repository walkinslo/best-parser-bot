from telegram import Update
from telegram.ext import ContextTypes

import message_texts
from .send_message import send_message

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_message(update, context, response = message_texts.HELP) 
