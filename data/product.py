import datetime
import sqlalchemy
from sqlalchemy import orm

from db_session import SqlAlchemyBase


class Product(SqlAlchemyBase):
    __tablename__ = 'products'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    photo_1 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    photo_2 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    photo_3 = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    descript = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    categories = orm.relation("ProductCategories")

class ProductCategories(SqlAlchemyBase):
    __tablename__ = 'productCategories'
    product_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    category_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    product = orm.relation("Product")