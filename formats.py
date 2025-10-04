from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def ask_disambiguation(options):
    kb = [[InlineKeyboardButton(text=o["label"], callback_data=o["payload"])] for o in options]
    return InlineKeyboardMarkup(inline_keyboard=kb)
