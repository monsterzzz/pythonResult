import sys,os
sys.path.append(os.getcwd())
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager,login_required
from datetime import timedelta


app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY']= "monster"   #设置为24位的字符,每次运行服务器都是不同的，所以服务器启动一次上次的session就清除。
app.config['PERMANENT_SESSION_LIFETIME']=timedelta(days=7) #设置session的保存时间。
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
login = LoginManager(app)

from engin import routes,models

