import sqlalchemy
from data.db_session import SqlAlchemyBase


class Department(SqlAlchemyBase):
    __tablename__ = 'department'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    chief = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), autoincrement=True)
    members = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String)
    creates_user_id = sqlalchemy.Column(sqlalchemy.Integer)
