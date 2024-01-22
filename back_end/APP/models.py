# /APP/models.py
# 模型 数据化相关
from .extends import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(30), unique=True)

    def is_active(self):  # line 37
        return True



