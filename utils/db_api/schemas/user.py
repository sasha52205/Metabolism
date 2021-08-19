from sqlalchemy import Integer, Column, BigInteger, String, sql

from utils.db_api.db_gino import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(100))
    gender = Column(String(100))
    age =Column(BigInteger)
    height = Column(BigInteger)
    weight = Column(BigInteger)
    activity = Column(String(100))
    target = Column(String(100))
    kkal = Column(BigInteger)
    today = Column(BigInteger)


    query: sql.Select
