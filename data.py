from pyrogram.types import InlineKeyboardButton

class Data:
    START = "Welcome! Click below to generate your string session."
    GENERATE_BUTTON = [[InlineKeyboardButton("Generate", callback_data="generate")]]
