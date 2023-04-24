import sqlalchemy
from .db_session import SqlAlchemyBase


class Article(SqlAlchemyBase):
    __tablename__ = 'articles'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    games = sqlalchemy.Column(sqlalchemy.Text)
    video_card = sqlalchemy.Column(sqlalchemy.Integer)
    cpu = sqlalchemy.Column(sqlalchemy.Integer)
    ram = sqlalchemy.Column(sqlalchemy.Integer)
    fps = sqlalchemy.Column(sqlalchemy.Integer)
