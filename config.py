class Config(object):
    """配置信息"""
    SECRET_KEY = "jiajia*jiajia~"

    # 数据库
    SQLALCHEMY_DATABASE_URI = "mysql://root:xxx@127.0.0.1:3306/sortweb"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """开发模式的配置信息"""
    DEBUG = True


class ProductionConfig(Config):
    """生产环境配置信息"""
    pass


# 这里做类名和名字对应关系。
# 创建一个creat_app 函数，工厂模式来创造咋样的app
# 它的配置信息到底是咋样的，app.config.from_object(？？？)就通过传递参数
config_map = {
    "develop": DevelopmentConfig,
    "product": ProductionConfig
}
