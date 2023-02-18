from telegram import InputMediaPhoto

def append_into_media_group(urls):
    media_group = []
    for url in urls:
        media = InputMediaPhoto(url)
        media_group.append(media)

    return media_group