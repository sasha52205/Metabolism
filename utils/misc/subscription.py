from typing import Union

from aiogram import Bot

from utils.db_api import quick_commands


async def check(user_id, channel: Union[int, str]):
    link = await quick_commands.select_link(id=1)
    bot = Bot.get_current()
    member = await bot.get_chat_member(user_id=user_id, chat_id=link.link)
    return member.is_chat_member()