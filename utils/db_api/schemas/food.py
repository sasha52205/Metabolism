from sqlalchemy import Integer, Column, BigInteger, String, sql

from utils.db_api.db_gino import TimedBaseModel


class Food(TimedBaseModel):
    __tablename__ = 'foods'
    id = Column(BigInteger, primary_key=True, auto_increment=True)
    name = Column(String(300))
    calories = Column(BigInteger)
    proteins =Column(BigInteger)
    fats = Column(BigInteger)
    carbohydrates = Column(BigInteger)




    query: sql.Select
