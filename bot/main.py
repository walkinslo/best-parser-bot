from API import *
from messages import * 

import logging
from typing import Dict

from os import getenv
from time import sleep

from telegram import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
    InputMediaPhoto
)
from telegram.ext import (
    Application, 
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters
)

logging.basicConfig(
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s", level = logging.INFO
)
logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = getenv("TELEGRAM_API_TOKEN")
if not TELEGRAM_API_TOKEN:
    exit("Please, specify the token env variable!")
