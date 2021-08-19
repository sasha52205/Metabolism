from sqlalchemy import Integer, Column, BigInteger, String, sql

from utils.db_api.db_gino import TimedBaseModel


class Link(TimedBaseModel):
    __tablename__ = 'links'
    id = Column(BigInteger, primary_key=True)
    link = Column(String(100))


    query: sql.Select