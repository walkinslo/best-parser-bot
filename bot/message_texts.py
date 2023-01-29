GREETING = """Hi! 
This bot will send you a lot of photos based on the tag that you provided.

Avaliable commands:

/start - this message
/tag - initiate a conversation with a bot related to tag and photos
/help - get help
"""


HELP = """My bot was created as a hobby, so it is a little bit buggy. 

Help me find those bugs by creating Issue token on github: https://github.com/walkinslo/best-parser-bot.

Commands:

/start - initial message
/tag - this command will initiate a conversation with bot, and it will try to find photos by the tag you provide. (No arguments, just /tag).
/help - display this message.
 
More command will be added soon so this message will be a little bit more useful.
"""


TAG = """Okay, to get photos specify tag - no commands needed, just type it after this message! 

For example: "boobs, 10".

Where "boobs" is your tag, and "10" is the amount of photos you want me to find.

I will try my best to find photos that have this tag.
"""


TAG_INVALID_INPUT = """
I was unable to read yor message.

Please, write your request like this:

boobs, 10

Where <b>boobs</b> is your tag, and <b>10</b> is the amount of photos you want to recieve.
"""


NO_TAG_ERROR = """
Oops! It looks like there is no such tag on Rule34.

Try another one!
"""