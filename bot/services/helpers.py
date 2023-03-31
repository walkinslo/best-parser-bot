import re

from telegram import InputMediaPhoto
from config import TAG_ELEMENTS_COUNT


def message_to_tag(user_message):
    return re.findall(r"(?<![\"=\w])(?:[^\W_]+)(?![\"=\w])", user_message)


def append_into_media_group(urls: list[str]) -> list:
    media_group = []
    for url in urls:
        media = InputMediaPhoto(url)
        media_group.append(media)

    return media_group


def _is_numbers_sufficient(numbers) -> bool:
    return len(numbers) == TAG_ELEMENTS_COUNT
