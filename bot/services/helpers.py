from telegram import InputMediaPhoto
from config import TAG_ELEMENTS_COUNT

def append_into_media_group(urls) -> list:
    media_group = []
    for url in urls:
        media = InputMediaPhoto(url)
        media_group.append(media)

    return media_group

def _is_numbers_sufficient(numbers: list[int]) -> bool:
    return len(numbers) == TAG_ELEMENTS_COUNT
