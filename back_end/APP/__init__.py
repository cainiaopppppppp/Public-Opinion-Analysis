# /APP/__init__.py
#初始化文件创建python应用
# import datetime

from flask import Flask
# from .views import blue
from .extends import *
from .urls import *
from .models import *
from .views import blue

def create_app() :
    app = Flask(__name__)
    app.static_folder = 'static'
    db_url = "mysql+pymysql://root:998994@localhost:3306/yq_db"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config['WTF_CSRF_ENABLED'] = False
    app.config["SECRET_KEY"] = secret_key
    app.register_blueprint(blue)  # 注册蓝图
    #SESSION过期时间
    # app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(days=7)
    init_exts(app)
    # 自定义指令 create 初始化数据库
    # @app.cli.command()
    # def create():
    #     db.drop_all()
    #     db.create_all()
    #     User.init_db()
    return app