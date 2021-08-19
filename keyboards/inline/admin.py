from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

cancel_mailing = InlineKeyboardMarkup(
    inline_keyboard=[
    [
        InlineKeyboardButton(text="Отмена", callback_data="no_mail")
    ]
    ]
)
cancel_change = InlineKeyboardMarkup(
    inline_keyboard=[
    [
        InlineKeyboardButton(text="Отмена", callback_data="no_change")
    ]
    ]
)


admin_kb = InlineKeyboardMarkup(
    inline_keyboard=[
    [
        InlineKeyboardButton(text="Рассылка", callback_data="mailing")
    ],
    [
        InlineKeyboardButton(text="Изменить канал", callback_data="change_link")
    ],
    [
        InlineKeyboardButton(text="Отмена", callback_data="exit_adm")
    ]

    ]
)