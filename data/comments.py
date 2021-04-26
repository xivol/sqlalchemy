import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Comments(SqlAlchemyBase):
    __tablename__ = 'comments'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"),
                                  nullable=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    connected_to_id = sqlalchemy.Column(sqlalchemy.Integer)
    table_name = sqlalchemy.Column(sqlalchemy.String)
    likes_count = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    empty = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    author = orm.relation('User')



    def date_str(self):
        return self.date.strftime('%Y/%b/%d/%H/%M')
