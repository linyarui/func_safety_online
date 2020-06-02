import os
from datetime import timedelta


class Config:
    ERROR_404_HELP = False

    SECRET_KEY = os.getenv('APP_SECRET', 'secret key')

    DB_USERNAME = 'root'
    DB_PASSWORD = 'root'
    DB_HOST = '127.0.0.1'
    DB_PORT = '3306'
    DB_NAME = 'func_safety_online'

    DB_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 100
    CSRF_ENABLED = True
    PERMANENT_SESSION_LIFETIME = timedelta(seconds=4 * 60 * 60)
    CMS_USER_ID = 'HEBOANHEHE'
    BACKEND_USER_ID = 'HEBOANHEHE'

    FILE_PATH = os.path.join(os.path.dirname(__file__), 'app\\static\\data')

    # mail
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = '465'
    MAIL_USE_SSL = True  # 使用SSL，端口号为465或587
    MAIL_USERNAME = '2237091767@qq.com'
    MAIL_PASSWORD = 'curivqbglcgodich'  # 注意，这里的密码不是邮箱密码，而是授权码
    MAIL_DEFAULT_SENDER = '2237091767@qq.com'  # 默认发送者


class DevConfig(Config):
    DEBUG = True


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    TESTING = True
    DEBUG = True


class ProdConfig(Config):
    DEBUG = False


config = {
    'development': DevConfig,
    'testing': TestConfig,
    'production': ProdConfig
}
