import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'xxx'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:hyr13551673998@localhost:3306/studentinfo'
    SQLALCHEMY_TRACK_MODIFICATIONS = False