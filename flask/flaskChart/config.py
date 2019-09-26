from datetime import timedelta

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/flask_dirty?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False
    SECRET_KEY = "helloworldmysession"
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)