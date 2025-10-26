from abc import abstractproperty
from flask import Flask,app,render_template,session,redirect,url_for,flash
from support import Pet,Cat,Dog
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,BooleanField,StringField,SubmitField,IntegerField,SelectField
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app=Flask(__name__)
bootstrap=Bootstrap(app)
app.config["SECRET_KEY"]="xxx"
app.config["SQLALCHEMY_DATABASE_URI"]="mysql+pymysql://root:hyr13551673998@localhost:3306/studentinfo"
db=SQLAlchemy(app)

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

class Major(db.Model):
    __tablename__ = 'majors'
    id = db.Column(db.Integer, primary_key=True)
    major_name = db.Column(db.String(100), unique=True, nullable=False)
    # 定义“一对多”关系中的“一”
    # 'students' 是反向引用的名称，'major' 是在 Student_Info 中定义的 backref 名称
    students = db.relationship('basicinfo', backref='major', lazy='dynamic')
    def __repr__(self):
        return f'<Major {self.major_name}>'

@app.route("/")
def index():
    students = basicinfo.query.all()
    majors = Major.query.all()
    return render_template("index.html", students=students, majors=majors)

@app.route("/delete/<id>", methods=["GET", "POST"])
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

