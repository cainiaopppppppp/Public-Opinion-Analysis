# /APP/extends.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS # 跨域
from flask_mail import Mail
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
api = Api()
cors = CORS()
mail = Mail()
login_manager = LoginManager()  # 实例化登录管理对象

def init_exts(app):
    db.init_app(app)
    migrate.init_app(app = app, db = db)
    api.init_app(app=app)
    cors.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)  # 初始化应用
    login_manager.login_view = 'login'  # 设置用户登录视图函数 endpoint
    login_manager.session_protection = "strong"