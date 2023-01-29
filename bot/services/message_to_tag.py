import re

def message_to_tag(user_message):
    return re.findall(r"(?<![\"=\w])(?:[^\W_]+)(?![\"=\w])", user_message)