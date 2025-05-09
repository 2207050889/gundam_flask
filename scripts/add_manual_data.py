#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
手动数据输入脚本
用于手动添加高达机体数据到数据库
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
        logging.FileHandler(os.path.join(BASE_DIR, 'scripts', 'manual_data.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('manual_data')

# 数据库配置
DB_PATH = os.path.join(BASE_DIR, 'instance', 'gundam.db')

# 手动添加的高达机体数据
GUNDAM_DATA = [
    {
        'name': 'RX-78-2 高达',
        'series': 'UC纪元',
        'year': 79,
        'pilot': '阿姆罗·雷',
        'height': 18.0,
        'weight': 60.0,
        'description': 'RX-78-2高达（RX-78-2 Gundam，日语：ガンダム）是日本动画《机动战士高达》中的主角机，由主角阿姆罗·雷驾驶。它是地球联邦军V作战计划中的第二号机，由地球联邦军的新型人类所驾驶，拥有非常强大的战斗力。它装备有射程远、命中率高的光束步枪，近战武器有热能军刀，还装有称为"盾"的类似方盾的防具，这在高达以前的MS（Mobile Suit，泛指具有人形形态的战争兵器）中是从未有过的装备。',
        'image_url': 'https://patchwiki.biligame.com/images/gundam/6/69/3r4l0rd37raqydxvuv1vxw3dhhzxxz3.png',
        'model_url': '/static/models/RX-78-2.stl'
    },
    {
        'name': 'MSZ-006 Z高达',
        'series': 'UC纪元',
        'year': 87,
        'pilot': '卡缪·维丹',
        'height': 19.9,
        'weight': 62.3,
        'description': 'Z高达（Z Gundam，日语：ゼータガンダム）是日本动画《机动战士Z高达》中的主角机体，由主角卡缪·维丹驾驶。它是由原属于地球联邦军（厌战派）的技术人员阿纳海姆研究所（ANAHEIM ELECTRONICS）技术人员在宇宙殖民地格利普斯（GRYPS）进行秘密开发的可变形MS。由于机体装备了复杂的武器控制程序，因此适合新人类驾驶。',
        'image_url': 'https://patchwiki.biligame.com/images/gundam/4/4e/63u01ufkw9c3qk7d8dr2nvqw7ahhb9z.png',
        'model_url': '/static/models/MSZ-006.stl'
    },
    {
        'name': 'ZGMF-X10A 自由高达',
        'series': 'SEED系列',
        'year': 71,
        'pilot': '基拉·大和',
        'height': 18.03,
        'weight': 71.5,
        'description': '自由高达（Freedom Gundam，日语：フリーダムガンダム），是日本动画《机动战士高达SEED》及其衍生作品中的机动战士，由主角基拉·大和驾驶。自由高达是由PLANTs最高评议会主席希尔德·克莱因下令，根据地球联合军开发的5台GAT-X系列高达为基础，秘密开发的5台机体中的一部。机体编号为ZGMF-X10A。',
        'image_url': 'https://patchwiki.biligame.com/images/gundam/0/08/jxjz6cxd9gy79w69f3edzkwfmtcmqbj.png',
        'model_url': '/static/models/ZGMF-X10A.stl'
    },
    {
        'name': 'ZGMF-X20A 强袭自由高达',
        'series': 'SEED系列',
        'year': 73,
        'pilot': '基拉·大和',
        'height': 18.88,
        'weight': 80.1,
        'description': '强袭自由高达（Strike Freedom Gundam，日语：ストライクフリーダムガンダム）是日本动画《机动战士高达SEED DESTINY》及其衍生作品中的机动战士，由主角基拉·大和驾驶。强袭自由高达是吉恩军高层所属的秘密机构"神鹰"计划中将要量产的机体中的一部。是由自由高达升级而来的高达机体，机体编号为ZGMF-X20A。',
        'image_url': 'https://patchwiki.biligame.com/images/gundam/4/48/j4lmjwvuatx89ywzkkqzm6qxkxqsvwz.png',
        'model_url': '/static/models/ZGMF-X20A.stl'
    },
    {
        'name': 'GN-001 能天使高达',
        'series': '00系列',
        'year': 2307,
        'pilot': '刹那·F·清英',
        'height': 18.3,
        'weight': 66.0,
        'description': '能天使高达（Gundam Exia，日语：ガンダムエクシア）是日本动画《机动战士高达00》中的主角机，由主角刹那·F·清英驾驶。配色以白色为主，辅以少量的蓝色点缀，在头部、胸部、肩部处采用了和传统高达相似的红、黄、蓝的配色，另外肩部、膝盖和脚部都有荧光绿色的部件。',
        'image_url': 'https://patchwiki.biligame.com/images/gundam/e/e5/d6fggb9h2eiey9iqqvwkvgwvbr9jwf7.png',
        'model_url': '/static/models/GN-001.stl'
    },
    {
        'name': 'GN-0000 00高达',
        'series': '00系列',
        'year': 2312,
        'pilot': '刹那·F·清英',
        'height': 18.3,
        'weight': 70.0,
        'description': '00高达（00 Gundam，日语：ダブルオーガンダム）是日本动画《机动战士高达00》第二季中的主角机，由主角刹那·F·清英驾驶。它是由两台GN-DRIVE作为动力源的机体，利用两台GN-DRIVE进行谐振，释放出的GN粒子是一般机体的数倍。',
        'image_url': 'https://patchwiki.biligame.com/images/gundam/0/03/atzitjl08b5yrp7fgofqkpjzsvpdx05.png',
        'model_url': '/static/models/GN-0000.stl'
    },
    {
        'name': 'XXXG-00W0 飞翼零式高达',
        'series': 'W系列',
        'year': 195,
        'pilot': '希罗·唯',
        'height': 16.7,
        'weight': 7.1,
        'description': '飞翼零式高达（Wing Gundam Zero，日语：ウイングガンダムゼロ）是日本动画《新机动战记高达W》中的机动战士，由主角希罗·唯驾驶。Wing Zero是由高达设计师卡多尔·桑德巴克博士所设计出的MS，伴随着"行动流星"的计划与开发而在此计划中成为被拒绝的幻之设计图。',
        'image_url': 'https://patchwiki.biligame.com/images/gundam/8/8b/g7dbfjcw0tawqo3mqcogw6c8a4kz5vq.png',
        'model_url': '/static/models/XXXG-00W0.stl'
    },
    {
        'name': 'RX-0 独角兽高达',
        'series': 'UC纪元',
        'year': 96,
        'pilot': '巴纳吉·林克斯',
        'height': 19.7,
        'weight': 42.7,
        'description': '独角兽高达（Unicorn Gundam，日语：ユニコーンガンダム）是日本动画《机动战士高达UC》中的主角机，由主角巴纳吉·林克斯驾驶。RX-0装备新型的精神感应框架，当NT驾驶员激活NT-D后，其体表会发生极大改变，通体紫红色发光，头部独角会像整流罩一样分开形成V字形，额头的感应框架暴露出来，肋部、后背、裙甲部份也会发生不同程度变化，所以也被一些人称作"可变形高达"。',
        'image_url': 'https://patchwiki.biligame.com/images/gundam/b/b2/dcofv7exv0zxd9aw6cm1j4bsktb3n6g.png',
        'model_url': '/static/models/RX-0.stl'
    },
    {
        'name': 'ASW-G-08 高达巴巴托斯',
        'series': '铁血系列',
        'year': 0,
        'pilot': '三日月·奥古斯',
        'height': 18.0,
        'weight': 30.5,
        'description': '高达巴巴托斯（Gundam Barbatos，日语：ガンダムバルバトス）是日本动画《机动战士高达 铁血的奥尔芬斯》中的主角机，由主角三日月·奥古斯驾驶。全名阿赫瓦塔·高达巴巴托斯，是72台高达机体中存在的第8台，是使用了古代文明的"阿赫瓦塔·高达"和为了顺应时代而在外部装上了装甲的高达。',
        'image_url': 'https://patchwiki.biligame.com/images/gundam/0/04/nvdpkxk9afuuhyuil79k38ixz1kwbh7.png',
        'model_url': '/static/models/ASW-G-08.stl'
    },
    {
        'name': 'MBF-P02 异端高达红色机',
        'series': 'SEED系列',
        'year': 71,
        'pilot': '洛萤·扎拉',
        'height': 17.53,
        'weight': 69.0,
        'description': '异端高达红色机（Gundam Astray Red Frame，日语：ガンダムアストレイレッドフレーム）是日本动画《机动战士高达SEED》及其衍生作品中的机动战士，由洛萤·扎拉驾驶。在亚丝娜·萨伊莫亲自监督之下，奥布"艾拉弗·法缇"组织完成了三台以GUNDAM为主构架的MS，以测试PS装甲的实用性。异端高达红色机是这其中的其中一架原型机，后被回收团队"准格尔"回收，并被洛萤·扎拉驾驶。',
        'image_url': 'https://patchwiki.biligame.com/images/gundam/7/78/0hhj7lwezb6v6hhcn5rw80c2q12r7q4.png',
        'model_url': '/static/models/MBF-P02.stl'
    }
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

def add_manual_data(conn):
    """
    添加手动输入的高达机体数据
    """
    cursor = conn.cursor()
    
    for gundam in GUNDAM_DATA:
        try:
            # 检查机体是否已存在
            cursor.execute("SELECT id FROM gundam WHERE name = ?", (gundam['name'],))
            existing = cursor.fetchone()
            
            if existing:
                # 更新已有记录
                cursor.execute("""
                    UPDATE gundam
                    SET series = ?, year = ?, pilot = ?, height = ?, weight = ?, 
                        description = ?, image_url = ?, model_url = ?
                    WHERE name = ?
                """, (
                    gundam['series'], gundam['year'], gundam['pilot'], 
                    gundam['height'], gundam['weight'], gundam['description'],
                    gundam['image_url'], gundam['model_url'], gundam['name']
                ))
                logger.info(f"更新机体记录: {gundam['name']}")
            else:
                # 插入新记录
                cursor.execute("""
                    INSERT INTO gundam (name, series, year, pilot, height, weight, description, image_url, model_url)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    gundam['name'], gundam['series'], gundam['year'],
                    gundam['pilot'], gundam['height'], gundam['weight'],
                    gundam['description'], gundam['image_url'], gundam['model_url']
                ))
                logger.info(f"添加新机体记录: {gundam['name']}")
            
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"保存机体 {gundam['name']} 数据失败: {e}")

def main():
    """
    主函数，执行手动数据添加
    """
    logger.info("开始手动添加高达机体数据")
    
    # 设置数据库
    conn = setup_database()
    
    try:
        # 添加手动数据
        add_manual_data(conn)
        
        logger.info("手动数据添加任务完成")
    except Exception as e:
        logger.error(f"手动数据添加过程中发生错误: {e}")
    finally:
        conn.close()
        logger.info("关闭数据库连接")

if __name__ == "__main__":
    main() 