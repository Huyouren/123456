from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from config import Config

# 全局实例化扩展，但不初始化
db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()

# 配置login_manager
login_manager.login_view = 'auth.login'
login_manager.login_message = '请先登录以访问此页面。'

def create_app():
    # 定义应用工厂
    app = Flask(__name__)
    app.config.from_object(Config)  # 从config.py加载配置

    # 使用init_app()方法延迟初始化扩展
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)

    # 注册蓝图
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')  # 认证蓝图，带/auth前缀

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)  # 主蓝图，不带前缀

    return app