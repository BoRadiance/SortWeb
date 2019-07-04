from flask import Flask
from config import config_map
from flask_sqlalchemy import SQLAlchemy
from App.utils.commons import ReConverter
from flask_wtf import CSRFProtect
db = SQLAlchemy()

# 工厂模式
def create_app(config_name):
    """
    创建flask的应用对象
    :param config_name: str  配置模式的模式的名字 （"develop",  "product"）
    :return:
    """
    app = Flask(__name__,static_url_path='/App/static')

    # 根据配置模式的名字获取配置参数的类
    config_class = config_map.get(config_name)
    app.config.from_object(config_class)

    # 什么时候app的一些设置结束了，我就什么时候初始化db
    # 使用app初始化db , 这个数据库对象很多python文件都要用的
    # 比如models.py 。你总要用来进行数据库操作。
    db.init_app(app)


    # 为flask添加自定义转换器
    app.url_map.converters["re"] = ReConverter

    # 注册蓝图
    from App import api_1_0
    app.register_blueprint(api_1_0.api, url_prefix="/api/v1.0")

    from App import web_html
    app.register_blueprint(web_html.html)


    return app