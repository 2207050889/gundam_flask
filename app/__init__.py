import os
from flask import Flask, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from config import Config
import logging

# 初始化扩展
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = '请先登录！'

def create_app(config_class=Config):
    # 创建Flask应用
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 配置日志
    logging.basicConfig(level=logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)
    
    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    
    # 注册蓝图
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    # 确保实例文件夹存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # 添加上下文处理器，在模板中提供系列列表
    @app.context_processor
    def inject_series_list():
        from app.models import Gundam
        # 获取系列列表
        try:
            series_list = db.session.query(Gundam.series).distinct().all()
            series_list = [s[0] for s in series_list] if series_list else []
        except:
            series_list = []
        return {'all_series': series_list}
    
    # 添加全局认证检查
    @app.before_request
    def check_login():
        # 如果用户未登录，并且请求的路径不是auth相关的路径，则重定向到登录页面
        if not current_user.is_authenticated:
            # 允许访问的路径列表
            allowed_paths = ['/auth/login', '/auth/register', '/static/']
            
            # 检查当前请求路径是否为允许路径
            current_path = request.path
            if not any(current_path.startswith(path) for path in allowed_paths):
                return redirect(url_for('auth.login'))
    
    return app

from app import models 