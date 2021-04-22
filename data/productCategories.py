import sqlalchemy
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase


class ProductCategories(SqlAlchemyBase):
     __tablename__ = 'productCategories'
     id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
     product_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("products.id"))
     category_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("categories.id"))
     product = orm.relation("Product")
     category = orm.relation("Categories")
