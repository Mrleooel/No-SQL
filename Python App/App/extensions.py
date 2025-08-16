from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
# 先初始化扩展（不依赖任何模型）
login_manager = LoginManager()
db = SQLAlchemy()
mongo = PyMongo()
def init_extensions(app):
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    db.init_app(app)
    mongo.init_app(app)