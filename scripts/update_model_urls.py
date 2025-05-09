#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
模型URL更新脚本
用于修复数据库中的模型URL路径
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
        logging.FileHandler(os.path.join(BASE_DIR, 'scripts', 'update_models.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('update_models')

# 数据库配置
DB_PATH = os.path.join(BASE_DIR, 'instance', 'gundam.db')

# 模型映射
MODEL_MAPPING = {
    'RX-78-2 高达': '/static/models/placeholder.stl',
    'MSZ-006 Z高达': '/static/models/placeholder.stl',
    'ZGMF-X10A 自由高达': '/static/models/placeholder.stl',
    'ZGMF-X20A 强袭自由高达': '/static/models/placeholder.stl',
    'GN-001 能天使高达': '/static/models/placeholder.stl',
    'GN-0000 00高达': '/static/models/placeholder.stl',
    'XXXG-00W0 飞翼零式高达': '/static/models/placeholder.stl',
    'RX-0 独角兽高达': '/static/models/placeholder.stl',
    'ASW-G-08 高达巴巴托斯': '/static/models/placeholder.stl',
    'MBF-P02 异端高达红色机': '/static/models/placeholder.stl'
}

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

def update_model_urls(conn):
    """
    更新数据库中的模型URL
    """
    cursor = conn.cursor()
    
    for name, model_url in MODEL_MAPPING.items():
        try:
            cursor.execute("""
                UPDATE gundam
                SET model_url = ?
                WHERE name = ?
            """, (model_url, name))
            
            if cursor.rowcount > 0:
                logger.info(f"更新机体 {name} 的模型URL为 {model_url}")
            else:
                logger.warning(f"未找到机体: {name}")
        except Exception as e:
            logger.error(f"更新机体 {name} 的模型URL失败: {e}")
    
    conn.commit()
    logger.info("模型URL更新完成")

def main():
    """
    主函数，执行模型URL更新
    """
    logger.info("开始更新模型URL")
    
    # 设置数据库
    conn = setup_database()
    
    try:
        # 更新模型URL
        update_model_urls(conn)
        
        logger.info("模型URL更新任务完成")
    except Exception as e:
        logger.error(f"模型URL更新过程中发生错误: {e}")
    finally:
        conn.close()
        logger.info("关闭数据库连接")

if __name__ == "__main__":
    main() 