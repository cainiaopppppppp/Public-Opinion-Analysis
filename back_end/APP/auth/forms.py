# /APP/auth/forms.py
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length, Email
from flask_wtf import FlaskForm


class RegisterForm(FlaskForm):
    username = StringField(label='用户名: ', validators=[DataRequired()])
    email = StringField(label='邮箱: ', validators=[DataRequired(), Email(message='邮箱格式错误')])
    password = PasswordField(label='密码: ', validators=[DataRequired(), Length(6, 16, message='密码格式错误')])


class LoginForm(FlaskForm):
    username = StringField(label='用户名: ', validators=[DataRequired()])
    password = PasswordField(label='密码: ', validators=[DataRequired(), Length(6, 16, message='密码格式错误')])

class ForgetForm(FlaskForm):
    email = StringField(label='邮箱: ', validators=[DataRequired(), Email(message='邮箱格式错误')])
    password = PasswordField(label='密码: ', validators=[DataRequired(), Length(6, 16, message='密码格式错误')])
