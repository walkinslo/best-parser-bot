from telegram import InlineKeyboardMarkup, InlineKeyboardButton

start_over = 1

def get_photos_keyboard(
        current_index: int, photos_count: list
) -> InlineKeyboardMarkup:

    prev_index = current_index - 1
    if prev_index < 0:
        prev_index = photos_count - 1
    next_index = current_index + 1
    if next_index > photos_count - 1:
        next_index = 0
    
    keyboard = [
        [
            InlineKeyboardButton(" < ", callback_data=f"{prev_index}"),
            InlineKeyboardButton(
                f"({current_index + 1}/{photos_count})", callback_data=" "
            ),
            InlineKeyboardButton(" > ", callback_data=f"{next_index}"), 
        ],
        [
            InlineKeyboardButton("Retrun", callback_data=str(start_over))
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
