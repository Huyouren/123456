from . import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, comment='登录用户名')
    password_hash = db.Column(db.String(512), nullable=False, comment='加密后的密码')
    is_admin = db.Column(db.Boolean, default=False, comment='是否为管理员')  # 用于区分权限

    # 密码加密存储
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    # 密码验证
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # 角色判断方法
    def is_admin(self):
        return self.is_admin

class Major(db.Model):
    __tablename__ = 'majors'
    id = db.Column(db.Integer, primary_key=True)
    major_name = db.Column(db.String(100), unique=True, nullable=False)
    # 定义“一对多”关系中的“一”
    students = db.relationship('basicinfo', backref='major', lazy='dynamic')
    
    def __repr__(self):
        return f'<Major {self.major_name}>'

class basicinfo(db.Model):
    __tablename__ = "basic_info"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='主键ID')
    student_id = db.Column(db.String(50), nullable=False, unique=True, comment='学生学号')
    student_name = db.Column(db.String(100), nullable=False, comment='学生姓名')
    student_sex = db.Column(db.String(10), nullable=True, comment='学生性别（文本描述）')
    is_male = db.Column(db.Boolean, nullable=True, comment='是否为男性（1:是，0:否）')
    create_time = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    年龄 = db.Column(db.Integer, default=11, comment='年龄') 
    major_id = db.Column(db.Integer, db.ForeignKey('majors.id'), comment='所属专业ID')

@login_manager.user_loader
def load_user(user_id):
    """通过用户ID从数据库加载用户对象"""
    return User.query.get(int(user_id))