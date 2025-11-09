
from abc import abstractproperty
from flask import Flask,app,render_template,session,redirect,url_for,flash
from support import Pet,Cat,Dog
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,BooleanField,StringField,SubmitField,IntegerField,SelectField
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import DataRequired, EqualTo, ValidationError
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from functools import wraps
from flask import abort
from flask_login import current_user


app=Flask(__name__)
bootstrap=Bootstrap(app)
app.config["SECRET_KEY"]="xxx"
app.config["SQLALCHEMY_DATABASE_URI"]="mysql+pymysql://root:hyr13551673998@localhost:3306/studentinfo"
db=SQLAlchemy(app)

# 初始化登录管理器（放在db初始化之后）
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # 指定登录页面路由
login_manager.login_message = '请先登录以访问该页面'  # 未登录访问受保护页面时的提示

# 用户认证模型（放在users表）
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
    def is_admin__(self):
        return self.is_admin
# class basicinfo(db.Model):
#     __tablename__="basicinfo"
#     id=db.Column(db.String(255),primary_key=True)
#     student_id=db.Column(db.String(255))
#     student_name=db.Column(db.String(255))
#     student_sex=db.Column(db.Boolean)
class basicinfo(db.Model):
    __tablename__ = "basic_info"  # 注意：数据库表名是 basic_info（带下划线），需与实际表名一致
    # 若表名确实是 basicinfo（无下划线），则保持 __tablename__ = "basicinfo"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='主键ID')
    student_id = db.Column(db.String(50), nullable=False, unique=True, comment='学生学号')
    student_name = db.Column(db.String(100), nullable=False, comment='学生姓名')
    student_sex = db.Column(db.String(10), nullable=True, comment='学生性别（文本描述）')
    is_male = db.Column(db.Boolean, nullable=True, comment='是否为男性（1:是，0:否）')
    create_time = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    年龄 = db.Column(db.Integer, default=11, comment='年龄') 
    # （其他字段保持不变）
    major_id = db.Column(db.Integer, db.ForeignKey('majors.id'), comment='所属专业ID')


    
class NameForm(FlaskForm):
    id = StringField("请输入学号：")
    name=StringField("请输入姓名：")
    sex=BooleanField("是否为男性")
    age=StringField("请输入年龄：")
    major = SelectField('Major', coerce=int)
    submit=SubmitField("提交")

class EditForm(FlaskForm):
    id = StringField("请输入学号：")
    name=StringField("请输入姓名：")
    sex=BooleanField("是否为男性")
    age=StringField("请输入年龄：")
    major = SelectField('Major', coerce=int)
    submit=SubmitField("提交")

# 在现有表单下方添加
class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')  # 任务三-3
    submit = SubmitField('登录')

class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    confirm_password = PasswordField('确认密码', validators=[
        DataRequired(),
        EqualTo('password', message='两次密码输入不一致')  # 任务二-4
    ])
    submit = SubmitField('注册')

    # 验证用户名唯一性（任务二-4）
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已被注册')


class Major(db.Model):
    __tablename__ = 'majors'
    id = db.Column(db.Integer, primary_key=True)
    major_name = db.Column(db.String(100), unique=True, nullable=False)
    # 定义“一对多”关系中的“一”
    # 'students' 是反向引用的名称，'major' 是在 Student_Info 中定义的 backref 名称
    students = db.relationship('basicinfo', backref='major', lazy='dynamic')
    def __repr__(self):
        return f'<Major {self.major_name}>'

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 改为调用新的方法名 is_admin()
        if not current_user.is_admin():
            flash('您没有权限执行此操作，请联系管理员', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# 登录用户加载回调函数
@login_manager.user_loader
def load_user(user_id):
    """通过用户ID从数据库加载用户对象"""
    return User.query.get(int(user_id))


@app.route("/")
def index():
    students = basicinfo.query.all()
    majors = Major.query.all()
    return render_template("index.html", students=students, majors=majors)

@app.route("/delete/<id>", methods=["GET", "POST"])
@admin_required  # 替换原@login_required
def delete(id):
    student = basicinfo.query.filter_by(student_id=id).first()
    if student is None:
        flash("该学生不存在！")
        return redirect(url_for("index"))
    form = FlaskForm()
    if form.validate_on_submit():
        db.session.delete(student)
        db.session.commit()
        flash("学生信息已成功删除！")
        return redirect(url_for("index"))
    
    return render_template("delete.html", form=form, student=student)

@app.route("/new",methods=["GET","POST"])
@admin_required  # 替换原@login_required
def new_student():
    form=NameForm()
    form.major.choices = [(m.id, m.major_name) for m in Major.query.order_by('major_name').all()]
    if form.validate_on_submit():
        id = form.id.data
        name=form.name.data
        sex = form.sex.data
        age = form.age.data
        major_obj = Major.query.get(form.major.data)
        new_student=basicinfo(student_name=name,student_id=id,is_male=sex,年龄=age,major=major_obj)
        db.session.add(new_student)
        db.session.commit()
        flash("添加成功！")
        return redirect(url_for("index"))
    return render_template("new.html",form=form)

@app.route("/edit/<id>", methods=["GET", "POST"])
@admin_required  # 替换原@login_required
def edit(id):
    student = basicinfo.query.filter_by(student_id=id).first()
    if student is None:
        flash("该学生不存在！")
        return redirect(url_for("index"))
    
    form = EditForm()  # 先初始化form
    form.major.choices = [(m.id, m.major_name) for m in Major.query.order_by('major_name').all()]
    
    if form.validate_on_submit():
        student.student_name = form.name.data
        student.is_male = form.sex.data
        student.年龄 = form.age.data
        student.major = Major.query.get(form.major.data)
        db.session.commit()
        flash("修改成功！")
        return redirect(url_for("index"))
    
    form.id.data = id
    form.name.data = student.student_name
    form.sex.data = student.is_male
    form.age.data = student.年龄
    form.major.data = student.major.id if student.major else None
    
    return render_template("edit.html", form=form)


@app.route("/major/<int:major_id>")
def filter_by_major(major_id):
    # 查找指定专业（不存在则返回404）
    major = Major.query.get_or_404(major_id)
    # 通过专业的反向引用查询该专业的所有学生（利用 Major 模型中定义的 students 关系）
    students = major.students.all()
    # 同时传递所有专业（用于显示筛选按钮）
    majors = Major.query.all()
    # 复用 index.html 模板，传入筛选后的学生列表
    return render_template('index.html', students=students, majors=majors)

# 登录页面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # 验证用户名和密码
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('用户名或密码错误')
            return redirect(url_for('login'))
        
        # 登录用户（记住我功能）
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    
    return render_template('login.html', form=form, title='登录')

#注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        # 创建新用户
        user = User(username=form.username.data)
        user.set_password(form.password.data)  # 加密存储密码
        db.session.add(user)
        db.session.commit()
        
        flash('注册成功，请登录！')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form, title='注册')

# 退出登录
@app.route('/logout')
@login_required  # 需登录才能访问
def logout():
    logout_user()
    flash('已成功退出登录')
    return redirect(url_for('index'))




@app.route("/<username>")
def user(username):
    return render_template("test2.html", username=username)

@app.route("/user")
def user_page():
    # 为导航栏的/user链接添加处理
    return redirect(url_for("hello2"))

@app.route("/hello/<name>")
def hello(name):
    comments=["a","b","c"]
    form=NameForm()
    form.name.data=name 
    return render_template("user.html",name=name,comments=comments,form=form)
@app.route("/hello",methods=["GET","POST"])
def hello2():
    form=NameForm()
    if form.validate_on_submit():
        oldname=session.get("name")
        if oldname is not None and oldname!=form.name.data:
            flash("您的姓名已经更新成功！")
        session["name"]=form.name.data
        return redirect(url_for("hello2"))
    return render_template("user.html",name=session.get("name"),form=form)

@app.route("/testvariables")
def testvariables():
    aCat=Cat("小白",2,"c波斯猫")
    aDog=Dog("旺财",2,"柴犬")
    return render_template("testvariables.html",aCat=aCat,aDog=aDog)
if __name__ == "__main__":
    app.run(debug=True)

