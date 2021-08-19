from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def create_link(link):
    check_button = InlineKeyboardMarkup(
    inline_keyboard=[
    [
        InlineKeyboardButton(text="Подписаться", url=link)
    ],
    [
        InlineKeyboardButton(text="Проверить подписку", callback_data="check_subs")
    ],
    ])
    return check_button


