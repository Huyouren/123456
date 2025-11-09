from flask import render_template, redirect, url_for, flash, request
from . import auth
from .. import db
from ..models import User
from ..forms import LoginForm, RegisterForm
from flask_login import login_user, logout_user, login_required, current_user

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # 验证用户名和密码
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('用户名或密码错误')
            return redirect(url_for('auth.login'))
        
        # 登录用户（记住我功能）
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    
    return render_template('login.html', form=form, title='登录')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已成功退出登录')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        # 创建新用户
        user = User(username=form.username.data)
        user.set_password(form.password.data)  # 加密存储密码
        db.session.add(user)
        db.session.commit()
        
        flash('注册成功，请登录！')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html', form=form, title='注册')