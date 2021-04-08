import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Managers(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'managers'

