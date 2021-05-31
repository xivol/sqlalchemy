import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Categories(SqlAlchemyBase):
    __tablename__ = 'categories'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    products = orm.relation("ProductCategories", back_populates="category")

    def __init__(self, title, content):
        self.title = title
        self.content = content
