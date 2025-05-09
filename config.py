import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    # 安全配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-gundam-secret-key'
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'gundam.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 应用配置
    GUNDAM_IMAGES_PER_PAGE = 9  # 每页显示的高达图片数量 