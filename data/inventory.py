import datetime
import sqlalchemy
from sqlalchemy import orm


from .db_session import SqlAlchemyBase


class Inventory(SqlAlchemyBase):
    __tablename__ = 'inventory'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    is_rented = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    arend_id = sqlalchemy.Column(sqlalchemy.String, default=0)
    condition = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')

