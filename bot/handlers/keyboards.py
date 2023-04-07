from telegram import InlineKeyboardMarkup, InlineKeyboardButton

start_over = 1

def get_photos_keyboard(
        current_index: int, 
        photos_count: list
) -> InlineKeyboardMarkup:
    
    keyboard = [
        [
            InlineKeyboardButton(" < ", callback_data=current_index - 1),
            InlineKeyboardButton(
                f"({current_index + 1}/{photos_count})", callback_data=" "
            ),
            InlineKeyboardButton(" > ", callback_data=current_index + 1), 
        ],
        [
            InlineKeyboardButton("Retrun", callback_data=str(start_over))
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
