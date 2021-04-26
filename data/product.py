import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Product(SqlAlchemyBase):
    __tablename__ = 'products'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    photo_1 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    photo_2 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    photo_3 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    descript = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Float, nullable=False)

    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

    categories = orm.relation("ProductCategories", back_populates="product")
