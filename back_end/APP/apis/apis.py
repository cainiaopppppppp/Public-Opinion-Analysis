# /APP/apis/apis.py
from flask import request, jsonify, redirect, render_template, url_for
from flask_restful import Resource
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.sql import and_, asc, desc, or_
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import jwt
from ..func import uid, mail
from ..models import User
from ..auth.forms import *
from ..extends import login_manager, db
from .__init__ import secret_key


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Login(Resource):
    def get(self):
        pass

    def post(self):
        login_form = LoginForm()
        if login_form.validate_on_submit():
            username = login_form.username.data
            password = login_form.password.data
            print(username, password)
            result = User.query.filter(User.username == username).first()
            print(result.password)
            if result and password == result.password:
                print("111")
                login_user(result)
                token = jwt.encode({
                    'user_uid': result.uid,
                    'username': username,
                    'user_id': result.id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=7)  # 设置 Token 过期时间
                }, secret_key, algorithm='HS256')
                return jsonify({"status": True, "token": token})  # 登录状态 True 成功 False 失败
            else:
                return jsonify({
                    "status": False,
                    "message": {
                        password: "wrong password"
                    }
                })
        else:
            return jsonify({
                "status": False,
                "message": login_form.errors
            })


class Logout(Resource):
    @login_required
    def get(self):
        logout_user()
        return redirect(url_for('login'))


class Register(Resource):
    def get(self):
        return jsonify({
            "status": True
        })

    def post(self):
        register_form = RegisterForm()
        print(1)
        if register_form.validate_on_submit():
            print(register_form)
            username = register_form.username.data
            password = register_form.password.data
            # password2 = request.form.get("password2")
            # hashed_password = generate_password_hash(password)
            email = register_form.email.data
            print(username)
            print(password)
            print(email)
            result = User.query.filter(or_(User.username == username, User.email == email)).first()
            # print(result)
            if result:
                return jsonify({
                    "status": False,
                    "message": {
                        "username": ["username or email is occupied"]
                    }
                })  # 注册失败 用户名或邮箱已占用
            else:
                user = User()
                user.username = username
                user.password = password
                user.email = email
                db.session.add(user)
                db.session.commit()

                print(user.id)
                UID = uid.IdWorker(user.id).get_id()
                user.uid = UID
                db.session.commit()
                return jsonify({"status": True})  # 注册成功
        else:
            return jsonify({
                "status": False,
                "message": register_form.errors
            })


class Forget(Resource):
    def post(self):
        forget_form = ForgetForm()
        if forget_form.validate_on_submit():
            new_password = forget_form.password.data
            email = forget_form.email.data
            result = User.query.filter(User.email == email).first()
            if result:
                result.password = new_password
                db.session.commit()
                return jsonify({
                    "status": True,
                    "message": 'success'
                })
            else:
                return jsonify({
                    "status": False,
                    "message": 'email dose not exist'
                })
        else:
            return jsonify({
                "status": False,
                "message": forget_form.errors
            })
