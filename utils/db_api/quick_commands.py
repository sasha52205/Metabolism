from asyncpg import UniqueViolationError

from utils.db_api.db_gino import db
from utils.db_api.schemas.links import Link
from utils.db_api.schemas.user import User
from utils.db_api.schemas.food import Food



async def add_user(id: int, name: str, gender:str = None, age: int = 0 , height: int= 0, weight: int= 0, activity:str = None, target: str = None, kkal:int = 0, today:int = 0):
    try:
        user = User(id=id, name=name, gender=gender, age=age, height=height, weight=weight, activity=activity, target=target, kkal=kkal, today=today)
        await user.create()

    except UniqueViolationError:
        pass


async def select_all_users():
    users = await User.query.gino.all()
    return users


async def select_user(id: int):
    user = await User.query.where(User.id == id).gino.first()
    return user


async def count_users():
    total = await db.func.count(User.id).gino.scalar()
    return total



async def update_user_gender(id, gender):
    user = await User.get(id)
    await user.update(gender=gender).apply()


async def update_user_age(id, age):
    user = await User.get(id)
    await user.update(age=age).apply()

async def update_user_height(id, height):
    user = await User.get(id)
    await user.update(height=height).apply()


async def update_user_weight(id, weight):
    user = await User.get(id)
    await user.update(weight=weight).apply()

async def update_user_activity(id, activity):
    user = await User.get(id)
    await user.update(activity=activity).apply()


async def update_user_target(id, target):
    user = await User.get(id)
    await user.update(target=target).apply()

async def update_user_kkal(id, kkal):
    user = await User.get(id)
    await user.update(kkal=kkal).apply()

async def update_user(id):
    user = await User.get(id)
    await user.update(kkal=0).apply()
    await user.update(gender=None).apply()
    await user.update(height=0).apply()
    await user.update(weight=0).apply()
    await user.update(activity=None).apply()
    await user.update(target=None).apply()


async def update_user_today(id, today):
    user = await User.get(id)
    await user.update(today=today).apply()


async def clear_user_today(id):
    user = await User.get(id)
    await user.update(today=0).apply()

###links
async def add_link(id: int = 1, link:str = None):
    try:
        link = Link(id=id, link=link)
        await link.create()

    except UniqueViolationError:
        pass

async def update_link(id, link):
    links = await Link.get(id)
    await links.update(link=link).apply()


async def select_link(id: int):
    link = await Link.query.where(Link.id == id).gino.first()
    return link


###foods
async def add_food(name: str,proteins:int = 0,fats:int = 0, carbohydrates: int = 0, calories: int = 0):
    try:
        food = Food(name=name,proteins=proteins,fats=fats,carbohydrates=carbohydrates, calories=calories)
        await food.create()

    except UniqueViolationError:
        pass
      


async def select_food_name(query):
    username = await db.select([Food]).where(Food.name.ilike(f"%{query.query}%")).gino.first()
    return username


async def select_food(id: int):
    food = await Food.query.where(Food.id == id).gino.first()
    return food