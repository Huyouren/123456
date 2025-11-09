from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField, SelectField, PasswordField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from .models import User

class NameForm(FlaskForm):
    id = StringField("请输入学号：", validators=[DataRequired()])
    name = StringField("请输入姓名：", validators=[DataRequired()])
    sex = BooleanField("是否为男性")
    age = StringField("请输入年龄：", validators=[DataRequired()])
    major = SelectField('专业', coerce=int)
    submit = SubmitField("提交")

class EditForm(FlaskForm):
    id = StringField("请输入学号：", validators=[DataRequired()])
    name = StringField("请输入姓名：", validators=[DataRequired()])
    sex = BooleanField("是否为男性")
    age = StringField("请输入年龄：", validators=[DataRequired()])
    major = SelectField('专业', coerce=int)
    submit = SubmitField("提交")

class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    confirm_password = PasswordField('确认密码', validators=[
        DataRequired(),
        EqualTo('password', message='两次密码输入不一致')
    ])
    submit = SubmitField('注册')

    # 验证用户名唯一性
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已被注册')