import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Arend(SqlAlchemyBase):
    __tablename__ = 'arend'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    status = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')

    object_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("inventory.id"))
    inventory = orm.relationship('Inventory')