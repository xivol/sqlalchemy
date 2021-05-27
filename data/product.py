import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Product(SqlAlchemyBase):
    __tablename__ = 'products'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    photo_1 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    photo_2 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    photo_3 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    descript = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    is_featured = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)
    rating = sqlalchemy.Column(sqlalchemy.Float, default= 0, nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

    categories = orm.relation("ProductCategories", back_populates="product")

    def __init__(self, title, descr, photo, price, is_featured):
        self.title = title
        self.descript = descr
        self.photo_1 = photo
        self.price = price
        self.is_featured = is_featured
