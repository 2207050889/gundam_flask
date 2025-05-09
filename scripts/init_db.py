#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库初始化脚本
用于创建数据库表结构
"""

import os
import sys
import logging
import sqlite3

# 设置基本路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(BASE_DIR, 'scripts', 'db_init.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('db_init')

# 数据库配置
DB_PATH = os.path.join(BASE_DIR, 'instance', 'gundam.db')

# 表结构SQL
CREATE_TABLES_SQL = [
    """
    CREATE TABLE IF NOT EXISTS gundam (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        series TEXT NOT NULL,
        year INTEGER,
        pilot TEXT,
        height REAL,
        weight REAL,
        description TEXT,
        image_url TEXT,
        model_url TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS comment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        user_id INTEGER NOT NULL,
        gundam_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES user (id),
        FOREIGN KEY (gundam_id) REFERENCES gundam (id)
    )
    """
]

# 测试账号数据
SAMPLE_USERS = [
    ('admin', 'admin@example.com', 'pbkdf2:sha256:150000$cEcr5Y6u$ea936d43e1e13816c87c7df011a35e14ec55ea2e19451bd6049d992271ae956f'),  # 密码: admin123
    ('test_user', 'test@example.com', 'pbkdf2:sha256:150000$B1Cjcs6r$1ea7d88738696aaefe2a49dc104d10b47cd640000fa4395ee7e8b4a227c0c7df')   # 密码: test123
]

def setup_database():
    """
    设置并初始化数据库
    """
    # 确保instance目录存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    # 连接到数据库
    conn = sqlite3.connect(DB_PATH)
    logger.info(f"成功连接到数据库: {DB_PATH}")
    
    return conn

def create_tables(conn):
    """
    创建数据库表
    """
    cursor = conn.cursor()
    
    for sql in CREATE_TABLES_SQL:
        try:
            cursor.execute(sql)
            logger.info(f"执行SQL: {sql[:60]}...")
        except Exception as e:
            logger.error(f"创建表失败: {e}")
    
    conn.commit()
    logger.info("数据库表结构创建完成")

def add_sample_data(conn):
    """
    添加示例数据
    """
    cursor = conn.cursor()
    
    # 添加测试用户
    try:
        for username, email, password_hash in SAMPLE_USERS:
            cursor.execute("""
                INSERT OR IGNORE INTO user (username, email, password_hash)
                VALUES (?, ?, ?)
            """, (username, email, password_hash))
        
        conn.commit()
        logger.info("添加测试用户数据完成")
    except Exception as e:
        conn.rollback()
        logger.error(f"添加测试用户数据失败: {e}")

def main():
    """
    主函数，执行数据库初始化
    """
    logger.info("开始数据库初始化任务")
    
    # 设置数据库
    conn = setup_database()
    
    try:
        # 创建表结构
        create_tables(conn)
        
        # 添加示例数据
        add_sample_data(conn)
        
        logger.info("数据库初始化任务完成")
    except Exception as e:
        logger.error(f"数据库初始化过程中发生错误: {e}")
    finally:
        conn.close()
        logger.info("关闭数据库连接")

if __name__ == "__main__":
    main() 