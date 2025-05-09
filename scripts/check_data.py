#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据检查脚本
用于查询并验证数据库中的数据
"""

import os
import sys
import logging
import sqlite3
from tabulate import tabulate

# 设置基本路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(BASE_DIR, 'scripts', 'check_data.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('check_data')

# 数据库配置
DB_PATH = os.path.join(BASE_DIR, 'instance', 'gundam.db')

def setup_database():
    """
    设置并初始化数据库连接
    """
    # 确保instance目录存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    # 连接到数据库
    conn = sqlite3.connect(DB_PATH)
    logger.info(f"成功连接到数据库: {DB_PATH}")
    
    return conn

def check_gundam_data(conn):
    """
    检查高达机体数据
    """
    cursor = conn.cursor()
    
    # 检查高达机体数量
    cursor.execute("SELECT COUNT(*) FROM gundam")
    count = cursor.fetchone()[0]
    logger.info(f"数据库中共有 {count} 个高达机体记录")
    
    # 按系列统计
    cursor.execute("SELECT series, COUNT(*) FROM gundam GROUP BY series")
    series_counts = cursor.fetchall()
    
    series_table = [["系列", "数量"]]
    for series, count in series_counts:
        series_table.append([series, count])
    
    print("\n高达机体系列统计:")
    print(tabulate(series_table, headers="firstrow", tablefmt="grid"))
    
    # 检查详细数据
    cursor.execute("""
        SELECT id, name, series, pilot, height, weight 
        FROM gundam
        ORDER BY series, name
    """)
    gundams = cursor.fetchall()
    
    gundam_table = [["ID", "名称", "系列", "驾驶员", "高度(m)", "重量(t)"]]
    for gundam in gundams:
        gundam_table.append(gundam)
    
    print("\n高达机体数据:")
    print(tabulate(gundam_table, headers="firstrow", tablefmt="grid"))

def check_user_data(conn):
    """
    检查用户数据
    """
    cursor = conn.cursor()
    
    # 检查用户数量
    cursor.execute("SELECT COUNT(*) FROM user")
    count = cursor.fetchone()[0]
    logger.info(f"数据库中共有 {count} 个用户记录")
    
    # 查看用户详细信息
    cursor.execute("SELECT id, username, email, register_date FROM user")
    users = cursor.fetchall()
    
    user_table = [["ID", "用户名", "邮箱", "注册时间"]]
    for user in users:
        user_table.append(user)
    
    print("\n用户数据:")
    print(tabulate(user_table, headers="firstrow", tablefmt="grid"))

def main():
    """
    主函数，执行数据验证
    """
    logger.info("开始数据验证任务")
    
    try:
        # 检查tabulate是否安装
        import tabulate
    except ImportError:
        print("请先安装tabulate: pip install tabulate")
        sys.exit(1)
    
    # 设置数据库
    conn = setup_database()
    
    try:
        # 检查高达机体数据
        check_gundam_data(conn)
        
        # 检查用户数据
        check_user_data(conn)
        
        logger.info("数据验证任务完成")
    except Exception as e:
        logger.error(f"数据验证过程中发生错误: {e}")
    finally:
        conn.close()
        logger.info("关闭数据库连接")

if __name__ == "__main__":
    main() 