import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # MongoDB配置
    MONGO_URI = os.environ.get('MONGO_URI', "mongodb://localhost:27017/forum_db")
    MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME', "forum_db")

    # SQL Server配置（使用Windows身份验证）
    SQL_SERVER = os.environ.get('SQL_SERVER', "localhost")
    SQL_DB = os.environ.get('SQL_DB', "forum_db")  # 默认使用系统数据库,实际使用其他forum_db
    # SQL_USER = ""  # 留空表示 Windows 身份验证
    # SQL_PASSWORD = ""

    # SQLALCHEMY连接字符串
    SQLALCHEMY_DATABASE_URI = (
        f'mssql+pyodbc://{SQL_SERVER}/{SQL_DB}'
        '?driver=ODBC+Driver+17+for+SQL+Server'
        '&Trusted_Connection=yes'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
