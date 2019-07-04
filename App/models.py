from flask_sqlalchemy import SQLAlchemy
from . import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(32),unique=True)
    # 防止外部调用，设置成私用，但是数据库保持的明文
    # 其实完全可以使用md5加盐加密.
    _password = db.Column(db.String(32))
    user_cartoon = db.relationship('Cartoon',backref='user')

    def __str__(self):
        return self.name


class Cartoon(db.Model):
    __tablename__ = 'cartoon'
    id = db.Column(db.Integer, primary_key=True)
    notsort = db.Column(db.String(500))
    speed = db.Column(db.Float)
    user_cartoon = db.Column(db.Integer,db.ForeignKey('user.id'))
    cartoon_save = db.relationship('SaveCartoon',backref='cartoon')

    def __str__(self):
        return str(self.user_cartoon)+self.notsort+self.speed


class SaveCartoon(db.Model):
    __tablename__ = 'savecartoon'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    seat = db.Column(db.String(500))
    cartoon_save = db.Column(db.Integer,db.ForeignKey('cartoon.id'))

    def __str__(self):
        return self.seat

