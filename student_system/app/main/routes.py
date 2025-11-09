from flask import render_template, redirect, url_for, flash, abort
from . import main
from .. import db
from ..models import basicinfo, Major, User
from ..forms import NameForm, EditForm, FlaskForm
from flask_login import login_required, current_user
from functools import wraps

# 管理员权限装饰器
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('您没有权限执行此操作，请联系管理员', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@main.route("/")
def index():
    students = basicinfo.query.all()
    majors = Major.query.all()
    return render_template("index.html", students=students, majors=majors)

@main.route("/delete/<id>", methods=["GET", "POST"])
@admin_required
def delete(id):
    student = basicinfo.query.filter_by(student_id=id).first()
    if student is None:
        flash("该学生不存在！")
        return redirect(url_for("main.index"))
    form = FlaskForm()
    if form.validate_on_submit():
        db.session.delete(student)
        db.session.commit()
        flash("学生信息已成功删除！")
        return redirect(url_for("main.index"))
    
    return render_template("delete.html", form=form, student=student)

@main.route("/new",methods=["GET","POST"])
@admin_required
def new_student():
    form = NameForm()
    form.major.choices = [(m.id, m.major_name) for m in Major.query.order_by('major_name').all()]
    if form.validate_on_submit():
        id = form.id.data
        name = form.name.data
        sex = form.sex.data
        age = form.age.data
        major_obj = Major.query.get(form.major.data)
        new_student = basicinfo(student_name=name, student_id=id, is_male=sex, 年龄=age, major=major_obj)
        db.session.add(new_student)
        db.session.commit()
        flash("添加成功！")
        return redirect(url_for("main.index"))
    return render_template("new.html", form=form)

@main.route("/edit/<id>", methods=["GET", "POST"])
@admin_required
def edit(id):
    student = basicinfo.query.filter_by(student_id=id).first()
    if student is None:
        flash("该学生不存在！")
        return redirect(url_for("main.index"))
    
    form = EditForm()
    form.major.choices = [(m.id, m.major_name) for m in Major.query.order_by('major_name').all()]
    
    if form.validate_on_submit():
        student.student_name = form.name.data
        student.is_male = form.sex.data
        student.年龄 = form.age.data
        student.major = Major.query.get(form.major.data)
        db.session.commit()
        flash("修改成功！")
        return redirect(url_for("main.index"))
    
    form.id.data = id
    form.name.data = student.student_name
    form.sex.data = student.is_male
    form.age.data = student.年龄
    form.major.data = student.major.id if student.major else None
    
    return render_template("edit.html", form=form)

@main.route("/major/<int:major_id>")
def filter_by_major(major_id):
    # 查找指定专业（不存在则返回404）
    major = Major.query.get_or_404(major_id)
    # 通过专业的反向引用查询该专业的所有学生
    students = major.students.all()
    # 同时传递所有专业（用于显示筛选按钮）
    majors = Major.query.all()
    # 复用index.html模板，传入筛选后的学生列表
    return render_template('index.html', students=students, majors=majors)

@main.route("/<username>")
def user(username):
    return render_template("test2.html", username=username)

@main.route("/user")
def user_page():
    # 为导航栏的/user链接添加处理
    return redirect(url_for("main.hello2"))

@main.route("/hello/<name>")
def hello(name):
    comments = ["a", "b", "c"]
    form = NameForm()
    form.name.data = name 
    return render_template("user.html", name=name, comments=comments, form=form)

@main.route("/hello", methods=["GET", "POST"])
def hello2():
    form = NameForm()
    if form.validate_on_submit():
        oldname = session.get("name")
        if oldname is not None and oldname != form.name.data:
            flash("您的姓名已经更新成功！")
        session["name"] = form.name.data
        return redirect(url_for("main.hello2"))
    return render_template("user.html", name=session.get("name"), form=form)

@main.route("/testvariables")
def testvariables():
    from ...support import Cat, Dog  # 假设support.py在项目根目录
    aCat = Cat("小白", 2, "波斯猫")
    aDog = Dog("旺财", 2, "柴犬")
    return render_template("testvariables.html", aCat=aCat, aDog=aDog)