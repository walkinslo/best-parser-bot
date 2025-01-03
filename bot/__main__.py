import logging

import bot.message_texts
import bot.config

from bot.handlers.response import send_message
from bot.handlers import start, help
from bot.handlers.buttons import pagination_button
from bot.handlers.tag_conv_handler import (
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
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TAG, SHOW_PHOTO = range(2)

if not bot.config.TELEGRAM_API_TOKEN:
    exit("Please, specify the token env variable!")


async def tag_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await send_message(update, context, response=bot.message_texts.TAG)

    return TAG


def main() -> None:
    application = (
        Application.builder()
        .concurrent_updates(True)
        .token(bot.config.TELEGRAM_API_TOKEN)
        .build()
    )

    tag_conv_handler = ConversationHandler(
        allow_reentry=True,
        entry_points=[CommandHandler("tag", tag_start)],
        states={
            TAG: [
                MessageHandler(filters.TEXT, tag)
            ],
            SHOW_PHOTO: [
                MessageHandler(filters.Regex("^(Show)$"), show_photo, block=False)
            ]
        },
        fallbacks=[CommandHandler("cancel", done)]
    )

    COMMAND_HANDLERS = {
        "start": start,
        "help": help
    }

    for command_name, command_handler in COMMAND_HANDLERS.items():
        application.add_handler(CommandHandler(command_name, command_handler))

    application.add_handler(tag_conv_handler)

    application.add_handler(CallbackQueryHandler(pagination_button))

    application.run_polling(drop_pending_updates=True)


try:
    main()
except Exception:
    import traceback

    logging.warning(traceback.format_exc())