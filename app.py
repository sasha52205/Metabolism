from utils.db_api.test import test
from utils.set_bot_commands import set_default_commands
from loader import db, scheduler
from utils.db_api import db_gino, quick_commands

#async def drop_today

#def scheduler_jobs():
#    scheduler.add_job(drop_today, 'cron', day_of_week='0-6',hour=23, minute=58)

async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)


    from utils.notify_admins import on_startup_notify
    print("Подключаем БД")
    await db_gino.on_startup(dp)
    print("Готово")

    print("Чистим базу")
    await db.gino.drop_all()

    print("Готово")

    print("Создаем таблицы")
    await db.gino.create_all()
    await quick_commands.add_link(1, "@clubhchat")
    print("Готово")
  #  await on_startup_notify(dp)
    await set_default_commands(dp)
    await test()
 #   scheduler.jobs()



if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

   # scheduler.start()

    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)


