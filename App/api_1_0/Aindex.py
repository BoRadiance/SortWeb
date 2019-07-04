# coding:utf-8

from flask import request, jsonify, current_app,session,render_template
from . import api
from App.models import User,Cartoon,SaveCartoon
from App import db
from sqlalchemy.exc import IntegrityError

class struct():
    pass


@api.route("/index")
def index():
    ret = [] # 最后返回的东西。
    us = User.query.all()
    for i in us:
        p = struct()
        p.name = i.name
        p.all = []
        # print(i.id)
        # print(i.name)
        # print('----')
        people = User.query.get(i.id)
        for car in people.user_cartoon:
            obj = struct()
            obj.id = car.id
            obj.notsort = car.notsort
            obj.speed = car.speed
            obj.pics = []
            gifs = Cartoon.query.get(obj.id)
            for gif in gifs.cartoon_save:
                pp = struct()
                pp.id = gif.id
                pp.name = gif.name
                pp.seat = gif.seat
                obj.pics.append(pp)
            p.all.append(obj)

        ret.append(p)


    # print('测试一下')
    # for i in ret:
    #     print("用户"+i.name)
    #     print('该用户生成的动画有')
    #     for j in i.all:
    #         print(j.notsort)
    #         print(j.speed)
    #         print('该动画拥有的动画为')
    #         for k in j.pics:
    #             print(k.id)
    #             print(k.name)
    #             print(k.seat)



    return render_template("aindex.html",data=ret)








from flask import make_response , send_file

@api.route('/download/<int:pid>', methods=['GET'])
def testdownload(pid):

    b = SaveCartoon.query.filter_by(id=pid).first()
    print(b.name)
    print(b.seat)
    filepath = "static/images/"+b.seat
    response = make_response(send_file(filepath))

    response.headers["Content-Disposition"] = "attachment; filename={}.gif".format(b.name)

    return response


