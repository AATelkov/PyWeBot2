import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    id_discord = sqlalchemy.Column(sqlalchemy.Integer)
    name = sqlalchemy.Column(sqlalchemy.Text)
    favorite_games = sqlalchemy.Column(sqlalchemy.Text)
    completed_games = sqlalchemy.Column(sqlalchemy.Text)
    video_card = sqlalchemy.Column(sqlalchemy.Integer)
    cpu = sqlalchemy.Column(sqlalchemy.Integer)
    ram = sqlalchemy.Column(sqlalchemy.Integer)
