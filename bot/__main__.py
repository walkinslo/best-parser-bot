import logging

import handlers
import config
import message_texts

from conv_handlers.tag_conv_handler import (
   tag,
   show_photo,
   done
)
from services.photos import button

from telegram import Update
from telegram.ext import (
    Application, 
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)
from telegram.constants import ParseMode

logging.basicConfig(
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level = logging.INFO
)
logger = logging.getLogger(__name__)


TAG, SHOW_PHOTO = range(2)


if not config.TELEGRAM_API_TOKEN:
    exit("Please, specify the token env variable!")


async def tag_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        text = message_texts.TAG,
        parse_mode=ParseMode.HTML
        )
    return TAG


def main() -> None:
    application = Application.builder().token(config.TELEGRAM_API_TOKEN).build()
    
    tag_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("tag", tag_start)],
        states = {
            TAG: [MessageHandler(filters.TEXT, tag)],
            SHOW_PHOTO: [MessageHandler(filters.Regex("^(Show)$"), show_photo)]
        },
        fallbacks=[MessageHandler(filters.Regex("^(Done|No|Cancel)$"), done)],
    )

    COMMAND_HANDLERS = {
        "start": handlers.start,
        "help": handlers.help
    }

    for command_name, command_handler in COMMAND_HANDLERS.items():
        application.add_handler(CommandHandler(command_name,command_handler))

    application.add_handler(tag_conv_handler)

    application.add_handler(CallbackQueryHandler(button))

    application.run_polling(drop_pending_updates=True)


try:
    main()
except Exception:
    import traceback
    
    logging.warning(traceback.format_exc())
