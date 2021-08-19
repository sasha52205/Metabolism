from aiogram import types
from aiogram.dispatcher.filters import Command, CommandStart


from loader import dp, bot
from utils.db_api import quick_commands
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery
from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


from keyboards.inline.metabolism import back_kb
from loader import dp
from states.Metabolism import Metabolism_state

@dp.inline_handler(text="")
async def empty_query(query: types.InlineQuery):
    await query.answer(
        results=[
            types.InlineQueryResultArticle(
                id="unknown",
                title="Начните вводить название продукта!",
                input_message_content=types.InputTextMessageContent(
                    message_text=f"Чтобы узнать калорийность продукта - начните вводить его название",
                    parse_mode="HTML"
                ),
            ),
        ],

        cache_time=5)




@dp.inline_handler()
async def empty_query(query: types.InlineQuery):
    food = await quick_commands.select_food_name(query)
    id =food.id
    await query.answer(
            results=[
                types.InlineQueryResultArticle(reply_markup=get_kb(id=id)
                                               id="none",
                                               title=f"{food.name}",
                                               input_message_content=types.InputTextMessageContent(
                                                   message_text=(f"<b>Название продукта:</b> {food.name}\n\n"
                                                                 f"<b>Белки:</b> {food.proteins} <b>Грамм</b>\n"
                                                                 f"<b>Жиры:</b> {food.fats} <b>Грамм</b>\n"
                                                                 f"<b>Углеводы:</b> {food.carbohydrates} <b>Грамм</b>\n\n"
                                                                 f"<b>Калорийность:</b> {food.calories} <b>Ккал</b>\n\n"
                                                                 f"<code> показатели на 100 грамм продукта</code>"

                                                                 ),
                                                   parse_mode="HTML",
                                               )
                                               ),
            ],

            cache_time=5)
kb_cd =CallbackData('food', 'id')


def get_kb(id):
    
        keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
    [
        InlineKeyboardButton(text="Другие граммовки", callback_data=kb_cd.new(id=id)
    ]
    ]
)
        return keyboard





@dp.callback_query_handler(keyboard.filter())
async def answer_gender(call: CallbackQuery, callback_data: dict, state: FSMContext):
    
    id =callback_data.get('id')
    await state.update_data(id=id)
    await state.set_state('id')


    await call.message.answer(f"Введите количество грамм продукта для расчёта!")





@dp.message_handler(state=Metabolism_state.age)
async def answer_age(message: types.Message, state: FSMContext):
    answer = message.text
   
    data = await state.get_data()
    id = data.get("id")
    food = await quick_commands.select_food(id=id)
    
    if answer.isdigit():
        calories1 = int(food.calories)/100
        proteins1 =int(food.proteins)/100
        fats1 =int(food.fats)/100
        carbohydrates1=int(food.carbohydrates)/100
        now_p = proteins1*int(answer)
        now_f =fats1*int(answer)
        now_c =carbohydrates1*int(answer)
        now_ccal = calories1*int(answer)
        await state.update_data(ccal=now_ccal)
        await message.answer(f'{food.name} - в {answer} граммах содержится:\n\n'
            f'Белки: {now_p}\n '
            f'Жиры: {now_f}\n'
            f'Углеводы: {now_c}\n\n'
            f'Калорийность: {now_ccal}',reply_markup=add_now_kb
            )
            await state.finish()
    else:
        await message.answer("Нужно ввести целое число !!!")
        return

    
add_now_kb= InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Отметить в дневной норме", callback_data="add_ccal"),

    ],
    [
        InlineKeyboardButton(text="Главное меню", callback_data="back")
    ]

])



@dp.callback_query_handler(text_contains='add_ccal')
async def answer_gender(call: CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    ccal = data.get('ccal')
    today = int(ccal)+int(user.today)
    await commands.update_user_today(id=call.from_user.id, today=int(today))

    user = await quick_commands.select_user(id=call.from_user.id)
    await call.message.edit_text(f"<b>Ваша дневная норма -</b> {user.kkal} ККал\n\n"
                             f"<b>Съеденно сегодня</b> {today} ККал\n\n"
                             f"<b>Осталось</b> {int(kkal)-int(today)} <b>ККал до дневной нормы</b>\n\n"
                            f"Чтобы перейти обратно в меню, нажмите на <b>кнопку</b>👇",reply_markup=back_kb)