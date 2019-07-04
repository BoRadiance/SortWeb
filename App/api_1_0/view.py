"""
这个主要写和动画有关系的视图函数
"""
import numpy as np
import matplotlib.pyplot as plt
import os
import shutil
import imageio
import time
import copy
from flask import request, jsonify, current_app,session,render_template,redirect
from . import api
from App.models import User,Cartoon,SaveCartoon
from App import db
from sqlalchemy.exc import IntegrityError
import re

#导入wtf扩展的表单类
from flask_wtf import FlaskForm
#导入自定义表单需要的字段
from wtforms import SubmitField,StringField,PasswordField
#导入wtf扩展提供的表单验证器
from wtforms.validators import DataRequired,EqualTo

class  aCartoon(FlaskForm):
    notsort = StringField(label=u'待排序数字',validators=[DataRequired()])
    speed = StringField(label=u'动画的速度',validators=[DataRequired()])
    submit = SubmitField(u'生成动画')

class UpdatePaswd(FlaskForm):
    pwd = StringField(label=u'修改密码',validators=[DataRequired()])
    submit = SubmitField(u'修改密码')


class struct():
    pass

userpath = ''
cartoon_id =-1
sorts = ['bubblesort', 'quicksort', 'insertsort', 'shellsort', 'selectsort', 'mergesort']


def check(path):
    '''
    创建临时保存每一帧图片的文件夹
    :param path: 路径名
    '''
    if not os.path.exists(path):
        # 如果没有path这个文件夹，那么我就创建。
        os.mkdir(path)
    else:
        # 如果有path这个文件夹，那我先删掉，再次创建。
        shutil.rmtree(path)
        os.mkdir(path)


def checkpath(path):
    """
    如果路径没有就创建
    :param path: 检查某用户的文件夹
    :return:
    """
    if not os.path.exists(path):
        os.mkdir(path)


def plotAndSave(X, Y, path):
    '''
    生成每一帧图片
    :param X:  X轴
    :param Y:  Y轴
    :param path: 图片的路径
    '''
    plt.cla()
    plt.bar(X, Y) # matplotlib 自带的画图， 参数都是2个列表， 一个做X轴，一个做Y轴。
    # 本来只要plt.show()就可以了。但是我们需要把图片保存起来
    # 所以需要用到savefig() 参数是保存的路径。 eg : ./PNG/0.png
    plt.savefig(path)



# 冒泡排序
def BubbleSort(size,speed,Arr):
    print('正在生成冒泡排序算法gif动画...')
    Xz = list(range(size))   # 根据长度来生成一个列表，这个列表用来做X轴
    path = './PNG'  # 指定一个临时存放图片的文件夹
    check(path) # 检查指定的路径文件夹
    Pngs = [] # 保存所有生成的图片的路径 eg ./PNG/1.png

    start_time = time.time()


    # 我们先把初始的数组样子画出来

    times =0 # 保存这次生成到哪张图片了。
    Pngs.append(os.path.join(path, str(times) + '.png')) #
    times += 1 # times肯定是要加一的，不然下一张图片岂不是覆盖了之前的图片。
    plotAndSave(Xz,Arr,Pngs[-1])
    # 原始的数组样子肯定是要画出来的。 保持的图片名为 0.png
    # 这个图片保存在 ./PNG 里面
    # Pngs[-1] 是取Pngs列表里面的最后一个。 这个时候的最后一个当然是0.png


    # 接下来是冒泡排序的核心算法
    for i in range(0, size):
        for j in range(0, size - i - 1):
            if Arr[j] > Arr[j + 1]:
                Arr[j], Arr[j + 1] = Arr[j + 1], Arr[j]
                # 把每一步之后的Arr数组画条形图
                Pngs.append(os.path.join(path, str(times) + '.png'))
                plotAndSave(Xz,Arr,Pngs[-1])
                times += 1

    # 最后二句是把最后一次的Arr数组的样子画出来。
    Pngs.append(os.path.join(path, str(times) + '.png'))
    plotAndSave(Xz, Arr, Pngs[-1])

    generated_images = []

    # 遍历Pngs里面的每张图片，把每张图片通过imageio.imread()读入
    # 然后把读入的每张图片的都
    for png_path in Pngs:
        generated_images.append(imageio.imread(png_path))

    # 加上这句话只是为了把最后一次图片多加上几遍，保险而已。
    generated_images = generated_images + [generated_images[-1]] * 5

    # 通过imageio.mimsave() 生成gif 参数： 名字，图片列表，格式，速度
    imageio.mimsave(sorts[0] + '.gif', generated_images, 'GIF', duration=speed)
    end_time = time.time()
    shutil.rmtree(path) # 删掉生成的临时文件夹

    print('冒泡排序算法gif动画已生成 耗时为 %f 秒，请查看当前路径的bubblesort.gif'%(end_time-start_time))
    if  os.path.exists(userpath+'/bubblesort.gif'):
        os.remove(userpath+'/bubblesort.gif')
    shutil.move('bubblesort.gif', userpath)
    global cartoon_id
    saveobj = SaveCartoon(name='bubblesort.gif',seat=userpath[45:]+'/bubblesort.gif',cartoon_save=cartoon_id)
    db.session.add(saveobj)
    db.session.commit()
    # userpath[45:] # /hcb/1,33,5,4,323

    print('')


# 快速排序
def QuickSort(size,speed,Arr):
    print('正在生成快速排序算法gif动画...')
    Xz = list(range(size))
    path = './PNG'
    check(path)
    Pngs = []
    start_time = time.time()
    times = 0
    Pngs.append(os.path.join(path, str(times) + '.png'))
    times += 1
    plotAndSave(Xz, Arr, Pngs[-1])

    def quicksort(Xz,times,Pngs,Arr, l, r):
        if l >= r:
            return
        stack = [l, r]
        while stack:
            low = stack.pop(0)
            high = stack.pop(0)
            if high <= low:
                continue
            pivot = Arr[high]
            i = low - 1  ###初始值是-1
            for j in range(low, high + 1):
                ###如果小于pivot， 则交换，交换的目的是保证[l,i]都比pivot小
                if Arr[j] <= pivot:
                    i += 1
                    t = Arr[i]
                    Arr[i] = Arr[j]
                    Arr[j] = t
            stack.extend([low, i - 1, i + 1, high])
            # print(Arr)
            # print('这个时候的times' + str(times))
            Pngs.append(os.path.join(path, str(times) + '.png'))
            plotAndSave(Xz, Arr, Pngs[-1])
            times += 1

    quicksort(Xz,times,Pngs,Arr,0,size-1)


    generated_images = []

    for png_path in Pngs:
        generated_images.append(imageio.imread(png_path))

    generated_images = generated_images + [generated_images[-1]] * 5
    imageio.mimsave(sorts[1] + '.gif', generated_images, 'GIF', duration=speed)
    end_time = time.time()
    shutil.rmtree(path)

    print('快速排序算法gif动画已生成 耗时为 %f 秒，请查看当前路径的quicksort.gif' % (end_time - start_time))
    if os.path.exists(userpath + '/quicksort.gif'):
        os.remove(userpath + '/quicksort.gif')
    shutil.move('quicksort.gif', userpath)
    global cartoon_id
    saveobj = SaveCartoon(name='quicksort.gif', seat=userpath[45:] + '/quicksort.gif', cartoon_save=cartoon_id)
    db.session.add(saveobj)
    db.session.commit()
    print('')


# 插入排序
def InsertSort(size,speed,Arr):
    print('正在生成插入排序算法gif动画...')
    Xz = list(range(size))
    path = './PNG'
    check(path)
    Pngs = []
    start_time = time.time()
    times = 0
    Pngs.append(os.path.join(path, str(times) + '.png'))
    times += 1
    plotAndSave(Xz, Arr, Pngs[-1])

    for i in range(1, size):
        j = i
        target = Arr[i]
        Pngs.append(os.path.join(path, str(times) + '.png'))
        plotAndSave(Xz, Arr, Pngs[-1])
        times += 1
        while j > 0 and target < Arr[j - 1]:
            Arr[j] = Arr[j - 1]
            j = j - 1
        Arr[j] = target




    Pngs.append(os.path.join(path, str(times) + '.png'))
    plotAndSave(Xz, Arr, Pngs[-1])
    generated_images = []

    for png_path in Pngs:
        generated_images.append(imageio.imread(png_path))

    generated_images = generated_images + [generated_images[-1]] * 5
    imageio.mimsave(sorts[2] + '.gif', generated_images, 'GIF', duration=speed)
    end_time = time.time()
    shutil.rmtree(path)
    print('插入排序算法gif动画已生成 耗时为 %f 秒，请查看当前路径的insertsort.gif' % (end_time - start_time))
    if os.path.exists(userpath + '/insertsort.gif'):
        os.remove(userpath + '/insertsort.gif')
    shutil.move('insertsort.gif', userpath)
    global cartoon_id
    saveobj = SaveCartoon(name='insertsort.gif', seat=userpath[45:] + '/insertsort.gif', cartoon_save=cartoon_id)
    db.session.add(saveobj)
    db.session.commit()
    print('')


# 希尔排序
def ShellSort(size,speed,Arr):
    print('正在生成希尔排序算法gif动画...')
    Xz = list(range(size))
    path = './PNG'
    check(path)
    Pngs = []
    start_time = time.time()
    times = 0
    Pngs.append(os.path.join(path, str(times) + '.png'))
    times += 1
    plotAndSave(Xz, Arr, Pngs[-1])

    def shellinsert(arr, d,times,Pngs):
        n = len(arr)
        for i in range(d, n):
            j = i - d
            temp = arr[i]  # 记录要出入的数
            while (j >= 0 and arr[j] > temp):  # 从后向前，找到比其小的数的位置
                arr[j + d] = arr[j]  # 向后挪动
                j -= d
            if j != i - d:
                arr[j + d] = temp

            Pngs.append(os.path.join(path, str(times) + '.png'))
            plotAndSave(Xz, Arr, Pngs[-1])
            times += 1

        return times

    d = size // 2
    while d >= 1:
        times = shellinsert(Arr, d,times,Pngs)
        d = d // 2

    Pngs.append(os.path.join(path, str(times) + '.png'))
    plotAndSave(Xz, Arr, Pngs[-1])
    generated_images = []

    for png_path in Pngs:
        generated_images.append(imageio.imread(png_path))

    generated_images = generated_images + [generated_images[-1]] * 5
    imageio.mimsave(sorts[3] + '.gif', generated_images, 'GIF', duration=speed)
    end_time = time.time()
    shutil.rmtree(path)
    print('希尔排序算法gif动画已生成 耗时为 %f 秒，请查看当前路径的shellsort.gif' % (end_time - start_time))
    if os.path.exists(userpath + '/shellsort.gif'):
        os.remove(userpath + '/shellsort.gif')
    shutil.move('shellsort.gif', userpath)
    global cartoon_id
    saveobj = SaveCartoon(name='shellsort.gif', seat=userpath[45:] + '/shellsort.gif', cartoon_save=cartoon_id)
    db.session.add(saveobj)
    db.session.commit()
    print('')


# 选择排序
def SelectSort(size,speed,Arr):
    print('正在生成选择排序算法gif动画...')
    Xz = list(range(size))
    path = './PNG'
    check(path)
    Pngs = []
    start_time = time.time()
    times = 0
    Pngs.append(os.path.join(path, str(times) + '.png'))
    times += 1
    plotAndSave(Xz, Arr, Pngs[-1])


    for i in range(0, size- 1):
        minIndex = i
        for j in range(i + 1, size):  # 比较一遍，记录索引不交换
            if Arr[j] < Arr[minIndex]:
                minIndex = j
        if minIndex != i:  # 按索引交换
            (Arr[minIndex], Arr[i]) = (Arr[i], Arr[minIndex])
            Pngs.append(os.path.join(path, str(times) + '.png'))
            plotAndSave(Xz, Arr, Pngs[-1])
            times += 1

    Pngs.append(os.path.join(path, str(times) + '.png'))
    plotAndSave(Xz, Arr, Pngs[-1])
    generated_images = []

    for png_path in Pngs:
        generated_images.append(imageio.imread(png_path))

    generated_images = generated_images + [generated_images[-1]] * 5
    imageio.mimsave(sorts[4] + '.gif', generated_images, 'GIF', duration=speed)
    end_time = time.time()
    shutil.rmtree(path)
    print('选择排序算法gif动画已生成 耗时为 %f 秒，请查看当前路径的selectsort.gif' % (end_time - start_time))
    if os.path.exists(userpath + '/selectsort.gif'):
        os.remove(userpath + '/selectsort.gif')
    shutil.move('selectsort.gif', userpath)
    global cartoon_id
    saveobj = SaveCartoon(name='selectsort.gif', seat=userpath[45:] + '/selectsort.gif', cartoon_save=cartoon_id)
    db.session.add(saveobj)
    db.session.commit()
    print('')


# 归并排序
def MergeSort(size,speed,Arr):

    def merge(Xz, Arr, low, mid, height, Pngs,times):
        """合并两个已排序好的列表，产生一个新的已排序好的列表"""
        # 通过low,mid height 将[low:mid) [mid:height)提取出来
        left = Arr[low:mid]
        right = Arr[mid:height]

        k = 0  # left的下标
        j = 0  # right的下标
        result = []  # 保存本次排序好的内容
        # 将最小的元素依次添加到result数组中
        while k < len(left) and j < len(right):
            if left[k] <= right[j]:
                result.append(left[k])
                k += 1
            else:
                result.append(right[j])
                j += 1

        # 将对比完后剩余的数组内容 添加到已排序好数组中
        result += left[k:]
        result += right[j:]
        # 将原始数组中[low:height)区间 替换为已经排序好的数组
        Arr[low:height] = result
        # print(times)
        # print(Arr)
        Pngs.append(os.path.join(path, str(times) + '.png'))
        plotAndSave(Xz, Arr, Pngs[-1])
        times += 1
        return times



    print('正在生成归并排序算法gif动画...')
    Xz = list(range(size))
    path = './PNG'
    check(path)
    Pngs = []
    start_time = time.time()
    times = 0
    Pngs.append(os.path.join(path, str(times) + '.png'))
    times += 1
    plotAndSave(Xz, Arr, Pngs[-1])

    i = 1
    while i < len(Arr):
        low = 0
        while low < len(Arr):
            mid = low + i
            height = min(low + 2 * i, len(Arr))
            if mid < height:
                times = merge(Xz,Arr, low, mid, height, Pngs,times)
            low += 2 * i
        i *= 2


    Pngs.append(os.path.join(path, str(times) + '.png'))
    plotAndSave(Xz, Arr, Pngs[-1])
    generated_images = []

    for png_path in Pngs:
        generated_images.append(imageio.imread(png_path))

    generated_images = generated_images + [generated_images[-1]] * 5
    imageio.mimsave(sorts[5] + '.gif', generated_images, 'GIF', duration=speed)
    end_time = time.time()
    shutil.rmtree(path)
    print('归并排序算法gif动画已生成 耗时为 %f 秒，请查看当前路径的mergesort.gif' % (end_time - start_time))
    if os.path.exists(userpath + '/mergesort.gif'):
        os.remove(userpath + '/mergesort.gif')
    shutil.move('mergesort.gif', userpath)
    global cartoon_id
    saveobj = SaveCartoon(name='mergesort.gif', seat=userpath[45:] + '/mergesort.gif', cartoon_save=cartoon_id)
    db.session.add(saveobj)
    db.session.commit()
    print('')


@api.route("/admin",methods=["GET","POST"])
def admin():
    print("该用户的信息")
    # session["name"] = user.name
    # session["user_id"] = user.id
    name = session.get("name")
    user_id = session.get("user_id")

    print(name)
    print(user_id)


    form = aCartoon()
    form2 = UpdatePaswd()
    if (name == None):
        return render_template("admin.html", form=form,form2=form2, msg='请先登录，登录之后才能对动画增删查',flag=True)

    print(form.validate_on_submit())

    ret = []
    people = User.query.get(user_id)
    for car in people.user_cartoon:
        obj = struct()
        obj.id = car.id
        obj.notsort = car.notsort
        obj.speed = car.speed
        obj.pics = []
        gifs = Cartoon.query.get(obj.id)
        for gif in gifs.cartoon_save:
            p = struct()
            p.id = gif.id
            p.name = gif.name
            p.seat = gif.seat
            obj.pics.append(p)

        ret.append(obj)

    # print('打印测试')
    # for r in ret:
    #     print(r.id, end='--')
    #     print(r.notsort, end='--')
    #     print(r.speed)
    #     print('有这些动画：')
    #     for i in r.pics:
    #
    #         print(i.id)
    #         print(i.name)
    #         print(i.seat)
    #         print('--------')

    if form.validate_on_submit():
        print('验证通过')
        wtf_notsort = str(form.notsort.data)
        wtf_speed = float(form.speed.data)
        # print(wtf_notsort)
        # print(type(wtf_notsort))
        #
        # print(wtf_speed)
        # print(type(wtf_speed))
        strs = wtf_notsort.split(',')
        # print(strs)

        try:
            Arr = list(map(lambda x: int(x), strs))
        except ValueError:
            return render_template('message.html',
                                   msg='输入的参数有错误，请仔细请求，以英文逗号分隔，前后都是数字结尾')

        print(Arr)
        size =len(Arr)
        print(size)
        print(os.getcwd())
        global userpath
        userpath=os.getcwd()+'/App/static/images/'+name+'/'+wtf_notsort
        print(userpath)



        scartoon = Cartoon(notsort=wtf_notsort,speed=wtf_speed,user_cartoon=user_id)
        db.session.add(scartoon)
        db.session.commit()
        global cartoon_id
        cartoon_id = scartoon.id

        if not os.path.exists(userpath):
            os.makedirs(userpath)

        BubbleSort(int(size), wtf_speed, copy.deepcopy(Arr))

        QuickSort(int(size), wtf_speed, copy.deepcopy(Arr))

        InsertSort(int(size), wtf_speed, copy.deepcopy(Arr))

        ShellSort(int(size), wtf_speed, copy.deepcopy(Arr))

        SelectSort(int(size), wtf_speed, copy.deepcopy(Arr))

        MergeSort(int(size), wtf_speed, copy.deepcopy(Arr))

        # 重定向，刷新页面
        return redirect('http://127.0.0.1:5000/api/v1.0/admin')



    else:
        if form2.validate_on_submit():
            print('修改密码验证通过')
            wtf_pwd = str(form2.pwd.data)
            u = User.query.get(user_id)
            u._password=wtf_pwd
            db.session.commit()
            session.pop('name',None)
            session.pop('user_id',None)
            # 重定向，刷新页面
            return redirect('http://127.0.0.1:5000/api/v1.0/admin')

        if request.method=='GET':

            return render_template('admin.html',form=form,form2=form2,data=ret,msg='以下是你创建的动画记录，你可以进行删除操作，点击某个具体动画将下载gif',flag=False)



@api.route('/delete/<int:pid>',methods=['GET'])
def delete(pid):
    print('aaaa')

    print()

    gifs = Cartoon.query.get(pid)
    for gif in gifs.cartoon_save:
        print(gif.seat)
        delpath = os.getcwd() + '/App/static/images'+gif.seat
        if os.path.exists(delpath):
            os.remove(delpath)

    # 从数据库中删除记录
    db.session.delete(gifs)
    db.session.commit()

    # 重定向刷新页面
    return redirect('http://127.0.0.1:5000/api/v1.0/admin')




