import logging 

import message_texts
import config
from handlers.response import send_message
from handlers import start, help
from handlers.buttons import pagination_button, navigation_button
from handlers.tag_conv_handler import (
        tag,
        show_photo,
        done
)

from telegram import Update
from telegram.ext import (
        Application,
        CommandHandler,
        ContextTypes,
        MessageHandler,
        ConversationHandler,
        CallbackQueryHandler,
        filters
)

logging.basicConfig(
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level = logging.INFO
)
logger = logging.getLogger(__name__)


TAG, SHOW_PHOTO = range(2)


if not config.TELEGRAM_API_TOKEN:
    exit("Please, specify the token env variable!")


async def tag_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await send_message(update, context, response=message_texts.TAG)
    
    return TAG


def main() -> None:
    application = Application.builder().concurrent_updates(True).token(config.TELEGRAM_API_TOKEN).build()
    
    tag_conv_handler = ConversationHandler(
        entry_points = [CommandHandler("tag", tag_start)],
        states = {
            TAG: [MessageHandler(filters.TEXT, tag)],
            SHOW_PHOTO: [
                MessageHandler(filters.Regex("^(Show)$"), show_photo, block=False)
            ]
        }, 
        fallbacks=[MessageHandler(filters.Regex("^Cancel"), done)],
    )

    COMMAND_HANDLERS = {
        "start": start,
        "help": help
    }

    for command_name, command_handler in COMMAND_HANDLERS.items():
        application.add_handler(CommandHandler(command_name,command_handler))
    
    application.add_handler(tag_conv_handler)

    application.add_handler(CallbackQueryHandler(pagination_button))
    application.add_handler(CallbackQueryHandler(navigation_button))

    application.run_polling(drop_pending_updates=True)    

try:
    main()
except Exception:
    import traceback

    logging.warning(traceback.format_exc())
