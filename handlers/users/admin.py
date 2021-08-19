from asyncio import sleep

from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import StatesGroup, State

from keyboards.inline.admin import cancel_mailing, admin_kb, cancel_change
from utils.db_api import quick_commands as commands
# Фича для рассылки по юзерам (учитывая их язык)
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, CallbackQuery, InlineKeyboardButton

from data.config import admins
from loader import dp, bot

class Mailing(StatesGroup):
    Text = State()
    Language = State()
start_mailing = InlineKeyboardMarkup(
    inline_keyboard=[
    [
        InlineKeyboardButton(text="Начать рассылку", callback_data="start_mail")
    ],
    [
        InlineKeyboardButton(text="Отмена", callback_data="no_mail")
    ]
    ]
)


@dp.message_handler(Command("admin"), user_id=admins)
async def add_item(message: types.Message):
    print("admin")
    count =await commands.count_users()
    await message.answer(text=f"<b>Меню администратора</b>\n\n"
                         f"Пользователей бота - <b>{count}</b>", reply_markup=admin_kb)


@dp.callback_query_handler(text_contains="exit_adm")
async def buying_pear(call: CallbackQuery):
    await call.message.delete()

@dp.callback_query_handler(text_contains="no_mail", state="*")
async def buying_pear(call: CallbackQuery, state: FSMContext):
    await call.answer("ВЫ отменили рассылку",show_alert=True)
    await call.message.edit_text("Вы отменили рассылку",reply_markup=admin_kb)
    await state.finish()



@dp.callback_query_handler(user_id=admins, text_contains="mailing")
async def mailing(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Пришлите текст рассылки", reply_markup=cancel_mailing)
    await Mailing.Text.set()


@dp.message_handler(user_id=admins, state=Mailing.Text)
async def mailing(message: types.Message, state: FSMContext):
    text = message.text
    await state.update_data(text=text)
    await message.answer(f"Текст рассылки:\n\n"
                         f"{text}",reply_markup=start_mailing)
    await Mailing.Language.set()


@dp.callback_query_handler(user_id=admins, state=Mailing.Language, text_contains="start_mail")
async def mailing_start(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get("text")
    await state.reset_state()
    await call.message.edit_reply_markup()

    users = await commands.select_all_users()
    for user in users:
        try:
            await bot.send_message(chat_id=user.id,
                                   text=text)
            await sleep(0.3)
        except Exception:
            pass
    await call.message.answer("Рассылка выполнена.")


####change link


@dp.callback_query_handler(text_contains="no_change", state="*")
async def buying_pear(call: CallbackQuery, state: FSMContext):
    await call.answer("Вы отменили изменение канала!", show_alert=True)
    await call.message.edit_text("Вы отменили изменение канала!",
                         reply_markup=admin_kb)
    await state.finish()

@dp.callback_query_handler(text_contains="change")
async def buying_pear(call: CallbackQuery, state: FSMContext):
    link = await commands.select_link(id=1)
    mm = await call.message.edit_text(f"На данный момент канал для подписки:\n\n"
                                 f"{link.link}\n\n"
                                 f"Пришлите юзернейм канала в ввиде @username\n"
                                 f"Или нажмите отмена",
                         reply_markup=cancel_change)
    mmm = mm.message_id
    await state.update_data(mmm=mmm)
    await state.set_state("change_link")


@dp.message_handler(state="change_link")
async def answer_age(message: types.Message, state: FSMContext):
    answer = str(message.text)
    print(answer)
    await commands.update_link(id=1,link=answer)
    data = await state.get_data()
    mmm = data.get("mmm")
    await bot.delete_message(chat_id=message.from_user.id, message_id=mmm)
    await message.answer(f"Канал для подписки изменен на::\n\n"
                                 f"{answer}\n\n")
    await state.finish()

