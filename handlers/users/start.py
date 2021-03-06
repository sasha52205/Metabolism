from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import channels
from keyboards.inline.subscribe import create_link
from loader import dp, bot
from utils.db_api import quick_commands as commands

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery
from emoji import emojize

from keyboards.inline.metabolism import metabolism_gender_markup, metabolism_activity_markup, activity_callback, \
    gender_callback, target_callback, metabolism_target_markup, global_menu, change_markup, back_kb
from loader import dp
from states.Metabolism import Metabolism_state
from utils.misc import metabolism_calculation, rate_limit, subscription


@dp.callback_query_handler(text_contains="yes")
async def buying_pear(call: CallbackQuery):
    user = await commands.select_user(id=call.from_user.id)
    await commands.update_user(id=call.from_user.id)
    await call.message.edit_text(f"<b>Укажите ваш пол:</b>",
                                 reply_markup=metabolism_gender_markup)


@dp.callback_query_handler(text_contains="no")
async def buying_pear(call: CallbackQuery):
    await call.message.edit_text("Используйте меню, для взаимодейвстия",
                         reply_markup=global_menu)

@dp.callback_query_handler(text_contains="back", state="*")
async def buying_pear(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Используйте меню, для взаимодейвстия",
                                      reply_markup=global_menu)
    await state.finish()

@dp.callback_query_handler(text_contains="today")
async def buying_pear(call: CallbackQuery, state: FSMContext):
    await call.answer()

    result = str()
    link = await commands.select_link(id=1)

    channel = link.link
    chat = await bot.get_chat(channel)
    links = await chat.export_invite_link()
    print(links)
    for channel in channels:
        status = await subscription.check(user_id=message.from_user.id, channel=channel)
        channel = await bot.get_chat(link.link)
        if status:
            user = await commands.select_user(id=call.from_user.id)
            kkal = user.kkal
            now = int(kkal) - int(user.today)
            if kkal == 0:
                await call.message.edit_text(f"<b>Для начала вам необходимо расчитать дневную норму калорий!</b>",
                                             reply_markup=global_menu)
            else:
                mess = await call.message.edit_text(
                    f"<code>Пришлите количество калорий съеденных за сегодня в цифрах (например 300).</code>\n\n"
                    f"<b>По результатам ваша дневная норма</b> {kkal} ККал\n\n"
                    f"<b>Съеденно за сегодня</b> {user.today} ККал\n"
                    f"<b>Осталось:</b> {now} ККал до дневной нормы\n\n"
                    f"Чтобы перейти обратно в меню, нажмите на <b>кнопку</b>👇\n", reply_markup=back_kb)

                m_id = mess.message_id
                await state.update_data(m_id=m_id)
                await state.set_state("today")
        else:
            # await message.answer(result, disable_web_page_preview=True)
            channels_format = str()
            for chat in channels:

                chat = await bot.get_chat(link.link)
                invite_link = await chat.export_invite_link()
                channels_format += f"Канал <a href='{invite_link}'>{chat.title}</a>\n\n"

                await call.message.answer(f"Привет, {call.from_user.first_name}! Чтобы воспользоваться ботом, тебе необходимо подписаться на канал \n"
                         f"👉 {channels_format}"
                         f"После подписки нажмите на кнопку '<b>Проверить подписку</b>'. Доступ будет открыт автоматически.",
                         reply_markup=create_link(link=links),
                         disable_web_page_preview=True)


@dp.message_handler(state="today")
async def answer_age(message: types.Message, state: FSMContext):
    answer = message.text
    print(answer)
    data=await state.get_data()
    m_id = data.get("m_id")
    print(m_id)
    user = await commands.select_user(id=message.from_user.id)
    kkal = user.kkal
    print(user.today)
    now = int(kkal) - int(user.today)

    if answer.isdigit():
        await commands.update_user_today(id=message.from_user.id, today=int(answer))
        # await bot.delete_message(message_id=m_id, chat_id=message.from_user.id)
        today = int(user.today)+int(message.text)
        await state.finish()
        if int(now) == 0:
            await bot.edit_message_text(message_id=m_id, chat_id=message.from_user.id,text=
            f"<b>По результатам, ваша дневная норма -</b> {kkal} ККал\n\n"
                                 f"<b>Съеденно сегодня</b> {today} ККал\n\n"
                                 f"<b>Вы уже съели дневную норму!</b>\n\n"
                                 f"Чтобы перейти обратно в меню, нажмите на <b>кнопку</b>👇",
                                reply_markup=back_kb)
        elif int(now) > int(kkal):
            await bot.edit_message_text(message_id=m_id, chat_id=message.from_user.id, text=
            f"<b>По результатам, ваша дневная норма -</b> {kkal} ККал\n\n"
                                 f"<b>Съеденно сегодня</b> {today} ККал\n\n"
                                 f"<b>Вы превысили дневную норму на</b> {int(kkal)-int(today)}!\n\n"
                                        f"Чтобы перейти обратно в меню, нажмите на <b>кнопку</b>👇",reply_markup=back_kb)
        else:
            await bot.edit_message_text(message_id=m_id, chat_id=message.from_user.id, text=
            f"<b>По результатам, ваша дневная норма -</b> {kkal} ККал\n\n"
                             f"<b>Съеденно сегодня</b> {today} ККал\n\n"
                             f"<b>Осталось</b> {int(kkal)-int(today)} <b>ККал до дневной нормы</b>\n\n"
                            f"Чтобы перейти обратно в меню, нажмите на <b>кнопку</b>👇",reply_markup=back_kb)
    else:
        await message.answer("Нужно ввести целое число или нажамите кнопку -  назад!")
        return



@dp.callback_query_handler(text_contains="count")
async def buying_pear(call: CallbackQuery):
    link = await commands.select_link(id=1)

    channel = link.link
    chat = await bot.get_chat(channel)
    links = await chat.export_invite_link()
    print(links)
    for channel in channels:
        status = await subscription.check(user_id=call.from_user.id, channel=channel)
        channel = await bot.get_chat(link.link)
        if status:
            user = await commands.select_user(id=call.from_user.id)
            kkal = user.kkal
            if user.kkal > 0:
                if user.target == "Сбросить вес":
                    prot = int(user.weight) * 2
                    fat = int(user.weight) * 0.5
                    ugleodi = int(user.weight) * 2.2
                elif user.target == "Набрать вес":
                    prot = int(user.weight) * 3.5
                    fat = int(user.weight) * 1
                    ugleodi = int(user.weight) * 3.2
                else:
                    prot = int(user.weight) * 2.5
                    fat = int(user.weight) * 0.7
                    ugleodi = int(user.weight) * 3.2
                await call.message.edit_text(
                    f"<b>Дневная норма для вас</b> - {kkal} ККал \n\n"
                    f"<b>Белки:</b> {prot}\n"
                    f"<b>Жиры:</b> {fat}\n"
                    f"<b>Углеводы:</b> {int(ugleodi)}\n")
                await call.message.answer("Уверены, что хотите изменить данные для измерения?",
                                          reply_markup=change_markup)
            else:
                await call.message.edit_text(
                    f"<b>Укажите ваш пол</b>",
                    reply_markup=metabolism_gender_markup)
        else:
            # await message.answer(result, disable_web_page_preview=True)
            channels_format = str()
            for chat in channels:
                chat = await bot.get_chat(link.link)
                invite_link = await chat.export_invite_link()
                channels_format += f"Канал <a href='{invite_link}'>{chat.title}</a>\n\n"

                await call.message.answer(
                f"Привет, {call.from_user.first_name}! Чтобы воспользоваться ботом, тебе необходимо подписаться на канал \n"
                f"👉 {channels_format}"
                f"После подписки нажмите на кнопку '<b>Проверить подписку</b>'. Доступ будет открыт автоматически.",
                reply_markup=create_link(link=links),
                disable_web_page_preview=True)


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    name = message.from_user.full_name
    await commands.add_user(id=message.from_user.id,
                            name=name)

    result = str()
    link = await commands.select_link(id=1)

    channel = link.link
    chat = await bot.get_chat(channel)
    links = await chat.export_invite_link()
    print(links)
    for channel in channels:
        status = await subscription.check(user_id=message.from_user.id, channel=channel)
        channel = await bot.get_chat(link.link)
        if status:
            # result += f"Подписка на канал <b>{channel.title}</b> Оформлена!\n\n"
            await message.answer("Используйте меню, для взаимодейвстия",
                                      reply_markup=global_menu)
        else:
            # await message.answer(result, disable_web_page_preview=True)
            channels_format = str()
            for chat in channels:

                chat = await bot.get_chat(link.link)
                invite_link = await chat.export_invite_link()
                channels_format += f"Канал <a href='{invite_link}'>{chat.title}</a>\n\n"

            await message.answer(f"Привет, {message.from_user.first_name}! Чтобы воспользоваться ботом, тебе необходимо подписаться на канал \n"
                         f"👉 {channels_format}"
                         f"После подписки нажмите на кнопку '<b>Проверить подписку</b>'. Доступ будет открыт автоматически.",
                         reply_markup=create_link(link=links),
                         disable_web_page_preview=True)

@dp.callback_query_handler(text="check_subs")
async def checker(call: types.CallbackQuery):
    await call.answer()
    link = await commands.select_link(id=1)
    result = str()
    channel = link.link
    chat = await bot.get_chat(channel)
    links = await chat.export_invite_link()

    for channel in channels:
        status = await subscription.check(user_id=call.from_user.id,
                                          channel=channel)
        channel = await bot.get_chat(link.link)
        if status:
            # result += f"Подписка на канал <b>{channel.title}</b> Оформлена!\n\n"
            await call.message.edit_text("Используйте меню, для взаимодейвстия",
                                 reply_markup=global_menu)
        else:
            await call.message.edit_text("<b>Для работы бота - вы должны быть подисанны на канал!</b>",reply_markup=create_link(link=links))
#    await call.message.edit_text(result, disable_web_page_preview=True, reply_markup=check_button)

# # @rate_limit(60, "metabolism")
# @dp.message_handler(Command("metabolism", prefixes="!/"), state=None)
# async def enter_test(message: types.Message):
#     await message.answer("Вы начали расчет своего уровня обмена веществ.\n"
#                          "Ваш пол?",
#                          reply_markup=metabolism_gender_markup)
#
#     # await Metabolism_state.gender.set()

@dp.callback_query_handler(target_callback.filter())
async def answer_gender(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)

    target = callback_data.get("value")
    await commands.update_user_target(target=target, id=call.from_user.id)
    user = await commands.select_user(id=call.from_user.id)
    description = callback_data.get("value")
    data = await state.get_data()
    m_id = data.get("m_id")
    await bot.delete_message(chat_id=call.from_user.id, message_id=m_id)
    mmm_id = await call.message.edit_text(f"<b>Ваш пол:</b> {user.gender}\n"
                                f"<b>Ваша цель:</b> {user.target}")
    m2_id = mmm_id.message_id
    await state.update_data(m2_id=m2_id)


    await call.message.answer(f"<b>Укажите ваш образ жизни:</b>", reply_markup=metabolism_activity_markup)

    # await Metabolism_state.weight.set()

@dp.callback_query_handler(gender_callback.filter())
# @dp.message_handler(state=Metabolism_state.gender)
async def answer_gender(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)

    gender = callback_data.get("value")
    await commands.update_user_gender(gender=gender, id=call.from_user.id)

    description = callback_data.get("description")
    await call.message.edit_text(
                                 f"<b>Ваш пол: {description}</b>\n")
    await call.message.answer(f"<b>Укажите вашу цель</b>", reply_markup=metabolism_target_markup)
    await state.update_data(m_id=call.message.message_id)
    # await call.message.answer(f"Укажите ваш уровень активности", reply_markup=metabolism_activity_markup)
    # await Metabolism_state.age.set()


@dp.message_handler(state=Metabolism_state.age)
async def answer_age(message: types.Message, state: FSMContext):
    answer = message.text
    user = await commands.select_user(id=message.from_user.id)
    data = await state.get_data()
    m_id = data.get("m2_id")
    activ = data.get("activ")

    if answer.isdigit():
        await commands.update_user_age(age=int(answer), id=message.from_user.id)
        await bot.edit_message_text(chat_id=message.from_user.id, message_id=m_id, text=
        f"<b>Ваш пол:</b> {user.gender}\n"
        f"<b>Ваша цель:</b> {user.target}\n"
        f"<b>Уровень вашей активности:</b> {activ}\n"
        f"<b>Ваш возраст: {message.text}</b>\n")
    else:
        await message.answer("Нужно ввести целое число !!!")
        return

    await message.answer(f"<b>Укажите ваш рост (в см):</b>")
    await Metabolism_state.height.set()

@dp.message_handler(state=Metabolism_state.height)
async def answer_height(message: types.Message, state: FSMContext):
    answer = message.text
    print(answer)
    user =await commands.select_user(id=message.from_user.id)
    data = await state.get_data()
    m_id = data.get("m2_id")
    print(m_id)
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=m_id, text=
                                 f"<b>Ваш пол:</b> {user.gender}\n"
                                 f"<b>Ваша цель:</b> {user.target}\n"
                                 f"<b>Уровень вашей активности:</b> {user.activity}\n"
                                 f"<b>Ваш возраст: {user.age}</b>\n"
                                 f"<b>Ваш рост: {answer}</b>")
    if answer.isdigit():
        await commands.update_user_height(height=int(answer), id=message.from_user.id)
    else:
        await message.answer("Нужно ввести целое число !!!")
        return

    await message.answer(f"<b>Укажите ваш вес (в кг):</b>")
    await Metabolism_state.weight.set()


@dp.message_handler(state=Metabolism_state.weight)
async def answer_weight(message: types.Message, state: FSMContext):
    answer = message.text
    data = await state.get_data()
    user = await commands.select_user(id=message.from_user.id)
    m_id = data.get("m2_id")
    activ = data.get("activ")
    print(m_id)
    await bot.delete_message(chat_id=message.from_user.id, message_id=m_id)
    # await message.answer(
    #                             text=f"<b>Расчет дневной нормы калорий</b>\n\n"
    #                                  f"<b>Ваш пол:</b> {user.gender}\n"
    #                                  f"<b>Ваша цель:</b> {user.target}\n"
    #                                  f"<b>Уровень вашей активности:</b> {activ}\n"
    #                                  f"<b>Ваш возраст: {user.age}</b>\n"
    #                                  f"<b>Ваш рост: {user.height}</b>\n"
    #                                  f"<b>Ваш вес: {message.text}</b>\n")


    if answer.isdigit():
        await commands.update_user_weight(weight=int(answer), id=message.from_user.id)
    else:
        await message.answer("Нужно ввести целое число !!!")
        return

    user = await commands.select_user(id=message.from_user.id)
    gender = user.gender  # пол мужской/женский
    age = user.age  # возраст, полных лет
    height = user.height  # рост, см
    weight = user.weight # вес, кг
    activity = float(user.activity)  # коэффициент уровня активности


    result = metabolism_calculation(gender=gender, age=age, height=height, weight=weight, activity=activity)
    print(result)
    user = await commands.select_user(id=message.from_user.id)
    if user.target == "Сбросить вес":
        kkal = int(result) - 300
        prot = int(user.weight)*2
        fat = int(user.weight)*0.5
        ugleodi = int(user.weight)*2.2
    elif user.target == "Набрать вес":
        kkal = int(result) + 400
        prot = int(user.weight) * 3.5
        fat = int(user.weight) * 1
        ugleodi = int(user.weight) * 3.2
    else:
        kkal = result
        prot = int(user.weight) * 2.5
        fat = int(user.weight) * 0.7
        ugleodi = int(user.weight) * 3.2
    await message.answer(f"<b>Ваш пол:</b> {user.gender}\n"
                         f"<b>Ваша цель:</b> {user.target}\n"
                         f"<b>Уровень вашей активности:</b> {activ}\n"
                         f"<b>Ваш возраст:</b> {user.age}\n"
                         f"<b>Ваш рост:</b> {user.height}\n"
                         f"<b>Ваш вес:</b> {message.text}\n\n"
                         f"<b>Результат</b>👇\n\n"
                         f"<b>Суточная норма потребления калорий для вашей цели составляет - </b>{kkal} <b>ККал</b> \n\n"
                         f"<b>Ориентировочное количество БЖУ для вашей цели:</b>\n\n"
                         f"Суточная норма белка - <b>{prot}</b> грамм \n\n"
                         f"Суточная норма жиров - <b>{fat}</b> грамм\n\n"
                         f"Суточная норма углеводов - <b>{int(ugleodi)}</b> грамм\n\n"
                         f"<code>Нажмите</code> /start <code> - для возвращения в меню!</code>"
                         )
    await commands.update_user_kkal(id=message.from_user.id, kkal=int(kkal))

    await state.finish()





@dp.message_handler(state=Metabolism_state.age)
async def answer_age(message: types.Message, state: FSMContext):
    answer = message.text
    data = await state.get_data()
    m_id = data.get("m_id")
    if answer.isdigit():
        await commands.update_user_age(age=int(answer), id=message.from_user.id)
    else:
        await message.answer("Нужно ввести целое число !!!")
        return
    user = await commands.select_user(id=message.from_user.id)
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=m_id,text=
                                 f"<b>Ваш пол:</b> {user.gender}\n"
                                 f"<b>Ваша цель:</b> {user.target}\n"
                                 f"<b>Уровень вашей активности:</b> {user.activity}"
                                 f"<b>Ваш возраст: {user.age}</b>")
    await Metabolism_state.height.set()
    # await state.finish()

@dp.callback_query_handler(activity_callback.filter())
# @dp.message_handler(state=Metabolism_state.activity)
async def answer_activity(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    user = await commands.select_user(id=call.from_user.id)
    coefficient = callback_data.get("coefficient")
    await commands.update_user_activity(activity=str(coefficient), id=call.from_user.id)
    description = callback_data.get("description")
    await state.update_data(activ=description)
    data = await state.get_data()
    m_id =  data.get("m2_id")
    print(m_id)
    await bot.edit_message_text(text=
                                 f"<b>Ваш пол:</b> {user.gender}\n"
                                 f"<b>Ваша цель:</b> {user.target}\n"
                                 f"<b>Уровень вашей активности:</b> {description}",
                                 chat_id=call.from_user.id, message_id=m_id)
    await call.message.edit_text(f'<b>Укажите ваш возраст:</b>')
    await Metabolism_state.age.set()
# description = callback_data.get("description")
#     await call.message.answer(text=f"{description}\n\n")
#     # Достаем переменные
#     user = await commands.select_user(id=call.from_user.id)
#     # data = await state.get_data()
#     # gender = data.get("gender")  # пол мужской/женский
#     # age = data.get("age")  # возраст, полных лет
#     # height = data.get("height")  # рост, см
#     # weight = data.get("weight")  # вес, кг
#     # activity = data.get("activity")  # коэффициент уровня активности
# ###########
#     gender = user.gender  # пол мужской/женский
#     age = user.age  # возраст, полных лет
#     height = user.height  # рост, см
#     weight = user.weight # вес, кг
#     activity = float(user.activity)  # коэффициент уровня активности
#     print(gender)
#     print(age)
#     print(height)
#     print(weight)
#     print(activity)
#
#     result = metabolism_calculation(gender=gender, age=age, height=height, weight=weight, activity=activity)
#
#     await call.message.answer(f"УРОВЕНЬ ВАШЕГО МЕТАБОЛИЗМА - {result} ККал \n\n")
#
#     await state.finish()



@dp.callback_query_handler(text="cancel")
async def cancel_buying(call: CallbackQuery, state: FSMContext):
    # Ответим в окошке с уведомлением!
    await call.answer(f"Вы не узнаете много нового о себе {emojize(':thinking_face:')}", show_alert=True)

    # Отправляем пустую клавиатуру изменяя сообщение
    await call.message.edit_reply_markup(reply_markup=None)

    await state.finish()
