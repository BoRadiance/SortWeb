"""
这里主要写和用户有关系的view视图函数
"""
from . import api
from App.models import User
from App import db
from sqlalchemy.exc import IntegrityError
from flask import request, jsonify, current_app,session,render_template,redirect
from App.models import User,Cartoon,SaveCartoon
#导入wtf扩展的表单类
from flask_wtf import FlaskForm
#导入自定义表单需要的字段
from wtforms import SubmitField,StringField,PasswordField
#导入wtf扩展提供的表单验证器
from wtforms.validators import DataRequired,EqualTo,Length


class regUser(FlaskForm):
    username = StringField(u'用户名', [DataRequired()])
    password = PasswordField(u'密码', [
        DataRequired(),
    ])
    confirm = PasswordField(u'确认密码',[DataRequired()])
    submit = SubmitField(u'注册')


class logUser(FlaskForm):
    username = StringField(u'用户名',[DataRequired()])
    password = PasswordField(u'密码',[DataRequired()])
    submit = SubmitField(u'登录')


@api.route("/register",methods = ["POST","GET"])
def register():

    form = regUser()

    if form.validate_on_submit():
        wtf_username = str(form.username.data)
        wtf_password = str(form.password.data)
        wtf_confirm = str(form.confirm.data)
        # print("账号"+wtf_username)
        # print("密码"+wtf_password)
        # print("确认密码"+wtf_confirm)
        if wtf_password!=wtf_confirm:
            return render_template('message.html',msg="二次输入的密码不一致，请重新注册")

        user = User(name=wtf_username,_password=wtf_password)
        db.session.add(user)
        db.session.commit()

        return redirect("login")

    if request.method=='GET':
        return render_template('register.html',form=form)



@api.route("/login",methods = ["POST","GET"])
def login():
    form = logUser()

    if form.validate_on_submit():
        wtf_username = str(form.username.data)
        wtf_password = str(form.password.data)

        user = User.query.filter_by(name=wtf_username).first()


        if user ==None:
            return render_template('message.html', msg="该用户不存在，请重新注册")

        if user._password != wtf_password:
            return render_template('message.html', msg="密码输入错误，请重新输入")

        session["name"] = user.name
        session["user_id"] = user.id
        return redirect('admin')

    if request.method=='GET':
        return render_template('login.html',form=form)
