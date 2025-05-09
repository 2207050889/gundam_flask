#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
高达机体数据收集脚本
用于从高达BWIKI网站爬取机体数据,并存储到SQLite数据库中
"""

import os
import re
import sys
import time
import json
import logging
import sqlite3
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 设置基本路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(BASE_DIR, 'scripts', 'data_collection.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('data_collector')

# 爬虫配置
BASE_URL = 'https://wiki.biligame.com/gundam/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 数据库配置
DB_PATH = os.path.join(BASE_DIR, 'instance', 'gundam.db')

# 高达系列分类
GUNDAM_SERIES = [
    'UC纪元',  # 宇宙世纪系列
    'SEED系列',  # SEED系列
    '00系列',  # 00系列
    'W系列',  # W系列
    'G系列',  # G高达系列
    'X系列',  # X系列
    'AGE系列',  # AGE系列
    '铁血系列',  # 铁血的奥尔芬斯系列
    '其他系列'  # 其他各种系列
]

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

def get_series_pages():
    """
    获取各个高达系列的页面URL
    """
    series_pages = []
    
    try:
        # 访问首页
        response = requests.get(BASE_URL, headers=HEADERS)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找所有作品链接
        works_section = soup.find('div', id='按作品检索')
        if works_section:
            works_links = works_section.find_all('a')
            for link in works_links:
                if link.get('href') and link.get('title'):
                    series_pages.append({
                        'title': link.get('title'),
                        'url': urljoin(BASE_URL, link.get('href'))
                    })
        
        logger.info(f"成功获取到 {len(series_pages)} 个高达系列页面")
    except Exception as e:
        logger.error(f"获取系列页面失败: {e}")
    
    return series_pages

def get_gundam_urls(series_url):
    """
    从系列页面中获取所有高达机体的URL
    """
    gundam_urls = []
    
    try:
        response = requests.get(series_url, headers=HEADERS)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找机体列表
        mecha_list = soup.find_all('a', href=re.compile(r'/gundam/.*'))
        for mecha in mecha_list:
            if '高达' in mecha.text or 'GUNDAM' in mecha.text.upper():
                gundam_urls.append({
                    'name': mecha.text,
                    'url': urljoin(BASE_URL, mecha.get('href'))
                })
        
        logger.info(f"从系列 {series_url} 中获取到 {len(gundam_urls)} 个高达机体URL")
    except Exception as e:
        logger.error(f"获取高达机体URL失败: {e}")
    
    return gundam_urls

def parse_gundam_details(gundam_url):
    """
    解析高达机体详情页面，提取所需信息
    """
    gundam_data = {
        'name': '',
        'series': '',
        'year': None,
        'pilot': '',
        'height': None,
        'weight': None,
        'description': '',
        'image_url': ''
    }
    
    try:
        response = requests.get(gundam_url['url'], headers=HEADERS)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 名称
        gundam_data['name'] = gundam_url['name']
        
        # 图片
        image_tag = soup.find('table', class_='wikitable').find('img')
        if image_tag and image_tag.get('src'):
            gundam_data['image_url'] = image_tag.get('src')
        
        # 系列
        for series in GUNDAM_SERIES:
            if series in response.text:
                gundam_data['series'] = series
                break
        
        # 从表格中提取信息
        info_table = soup.find('table', class_='wikitable')
        if info_table:
            rows = info_table.find_all('tr')
            for row in rows:
                header = row.find('th')
                value = row.find('td')
                if header and value:
                    header_text = header.text.strip()
                    value_text = value.text.strip()
                    
                    if '型号' in header_text:
                        # 型号信息通常在描述中展示
                        model_info = f"型号: {value_text}"
                        gundam_data['description'] += model_info + '\n'
                    elif '全高' in header_text or '高度' in header_text:
                        try:
                            # 提取数字，通常格式为 "18.5m"
                            height_match = re.search(r'(\d+\.?\d*)m', value_text)
                            if height_match:
                                gundam_data['height'] = float(height_match.group(1))
                        except:
                            pass
                    elif '重量' in header_text:
                        try:
                            # 提取数字，通常格式为 "58.7t"
                            weight_match = re.search(r'(\d+\.?\d*)t', value_text)
                            if weight_match:
                                gundam_data['weight'] = float(weight_match.group(1))
                        except:
                            pass
                    elif '驾驶员' in header_text or '搭乘者' in header_text:
                        gundam_data['pilot'] = value_text
                    elif '年代' in header_text:
                        try:
                            # 尝试提取年份
                            year_match = re.search(r'(\d+)', value_text)
                            if year_match:
                                gundam_data['year'] = int(year_match.group(1))
                        except:
                            pass
        
        # 提取描述信息
        description_section = soup.find('div', {'id': 'mw-content-text'})
        if description_section:
            paragraphs = description_section.find_all('p')
            for p in paragraphs:
                if len(p.text.strip()) > 50:  # 只取较长的段落作为描述
                    gundam_data['description'] += p.text.strip() + '\n'
                    if len(gundam_data['description']) > 500:
                        # 限制描述长度
                        gundam_data['description'] = gundam_data['description'][:500] + '...'
                        break
        
        logger.info(f"成功解析机体 {gundam_data['name']} 的详情")
    except Exception as e:
        logger.error(f"解析机体详情失败: {e}")
    
    return gundam_data

def save_to_database(conn, gundam_data):
    """
    将高达机体数据保存到数据库
    """
    try:
        cursor = conn.cursor()
        
        # 检查机体是否已存在
        cursor.execute("SELECT id FROM gundam WHERE name = ?", (gundam_data['name'],))
        existing = cursor.fetchone()
        
        if existing:
            # 更新已有记录
            cursor.execute("""
                UPDATE gundam
                SET series = ?, year = ?, pilot = ?, height = ?, weight = ?, 
                    description = ?, image_url = ?
                WHERE name = ?
            """, (
                gundam_data['series'], gundam_data['year'], gundam_data['pilot'],
                gundam_data['height'], gundam_data['weight'], gundam_data['description'],
                gundam_data['image_url'], gundam_data['name']
            ))
            logger.info(f"更新机体记录: {gundam_data['name']}")
        else:
            # 插入新记录
            cursor.execute("""
                INSERT INTO gundam (name, series, year, pilot, height, weight, description, image_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                gundam_data['name'], gundam_data['series'], gundam_data['year'],
                gundam_data['pilot'], gundam_data['height'], gundam_data['weight'],
                gundam_data['description'], gundam_data['image_url']
            ))
            logger.info(f"添加新机体记录: {gundam_data['name']}")
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error(f"保存到数据库失败: {e}")

def main():
    """
    主函数，协调整个数据收集过程
    """
    logger.info("开始高达机体数据收集任务")
    
    # 设置数据库
    conn = setup_database()
    
    try:
        # 获取系列页面
        series_pages = get_series_pages()
        
        total_gundams = 0
        # 处理每个系列
        for series in series_pages:
            logger.info(f"正在处理系列: {series['title']}")
            
            # 获取该系列中的所有机体URL
            gundam_urls = get_gundam_urls(series['url'])
            
            # 限制每个系列处理的机体数量，避免请求过多
            for gundam_url in gundam_urls[:10]:  # 每个系列最多处理10个机体
                logger.info(f"正在解析机体: {gundam_url['name']}")
                
                # 解析机体详情
                gundam_data = parse_gundam_details(gundam_url)
                
                # 保存到数据库
                save_to_database(conn, gundam_data)
                
                total_gundams += 1
                
                # 添加延时，避免请求过快
                time.sleep(1)
        
        logger.info(f"数据收集任务完成，共处理 {total_gundams} 个高达机体")
    except Exception as e:
        logger.error(f"数据收集过程中发生错误: {e}")
    finally:
        conn.close()
        logger.info("关闭数据库连接")

if __name__ == "__main__":
    main() 