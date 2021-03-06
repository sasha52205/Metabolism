
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

"""универсальная кнопка отмены на все случаи жизни

"""
cancel_button = InlineKeyboardButton(text="Отмена", callback_data="cancel")
cancel_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        cancel_button]
])

"""клавиатура выбора пола респондента

"""
gender_callback = CallbackData("gender", "description", "value")
target_callback = CallbackData("target", "value")

metabolism_gender_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Мужской", callback_data=gender_callback.new(description="Мужчина", value="Мужчина")),
        InlineKeyboardButton(text="Женский", callback_data=gender_callback.new(description="Женщина", value="Женщина"))
    ]
])


###############
global_menu= InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Начать расчет калорий", callback_data="count"),

    ],
    [
        InlineKeyboardButton(text="Отметить калории", callback_data="today")
    ],
    [
        InlineKeyboardButton(text="Калорийность продуктов", switch_inline_query_current_chat=""),
    ]

])

back_kb= InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Назад", callback_data="back"),

    ]
])
###############

change_markup= InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Да", callback_data="yes"),

    ],
    [
        InlineKeyboardButton(text="Нет", callback_data="no")
    ]
])
####Цель
metabolism_target_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Сбросить вес", callback_data=target_callback.new(value="Сбросить вес")),

    ],
    [
        InlineKeyboardButton(text="Поддерживать вес", callback_data=target_callback.new(value="Поддерживать вес"))
    ],
    [
        InlineKeyboardButton(text="Набрать вес", callback_data=target_callback.new(value="Набрать вес"))
    ]
])
"""клавиатура выбора активности респондента

"""
activity_callback = CallbackData("activity", "description", "coefficient")

metabolism_activity_markup = InlineKeyboardMarkup(row_width=1)

activities = list()

activities.append(
    InlineKeyboardButton(text="Сидячий образ жизни",
                         callback_data=activity_callback.new(
                             description="Сидячий образ жизни",
                             coefficient=1.2)
                         )
)

activities.append(
    InlineKeyboardButton(text="Умеренная активность",
                         callback_data=activity_callback.new(
                             description="Умеренная активность",
                             coefficient=1.4)
                         )
)

activities.append(
    InlineKeyboardButton(text="Тренировки 3-5 в неделю",
                         callback_data=activity_callback.new(
                             description="Тренировки 3-5 в неделю",
                             coefficient=1.5)
                         )
)

activities.append(
    InlineKeyboardButton(text="Интенсивные нагрузки",
                         callback_data=activity_callback.new(
                             description="Интенсивные нагрузки",
                             coefficient=1.75)
                         )
)

activities.append(
    InlineKeyboardButton(text="Профессиональные спортсмены",
                         callback_data=activity_callback.new(
                             description="Проф. спортсмены",
                             coefficient=1.9)
                         )
)





for activity in activities:
    metabolism_activity_markup.insert(activity)
