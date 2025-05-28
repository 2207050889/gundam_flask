#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sqlite3
from pathlib import Path

def test_background_system():
    """测试背景图片系统"""
    print("="*60)
    print("背景图片系统测试")
    print("="*60)
    
    # 检查数据库
    db_path = Path('./instance/gundam.db')
    if not db_path.exists():
        print("❌ 数据库文件不存在")
        return False
    
    # 检查图片目录
    images_dir = Path('./app/static/images/details')
    if not images_dir.exists():
        print("❌ 图片目录不存在")
        return False
    
    # 检查CSS文件
    css_file = Path('./app/static/css/gundam_backgrounds.css')
    if not css_file.exists():
        print("❌ 背景CSS文件不存在")
        return False
    
    # 获取机体列表
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM gundam ORDER BY id')
    gundams = cursor.fetchall()
    conn.close()
    
    # 获取图片文件
    image_files = [f.name for f in images_dir.glob('*.jpg')]
    
    print(f"✅ 数据库中有 {len(gundams)} 个机体")
    print(f"✅ 图片目录中有 {len(image_files)} 个图片文件")
    print(f"✅ CSS文件存在")
    
    # 检查模板文件
    template_file = Path('./app/templates/detail.html')
    if template_file.exists():
        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'bg-rx-78-2-gundam' in content:
                print("✅ detail.html模板已更新")
            else:
                print("❌ detail.html模板未正确更新")
    
    # 检查base.html
    base_file = Path('./app/templates/base.html')
    if base_file.exists():
        with open(base_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'gundam_backgrounds.css' in content:
                print("✅ base.html已引入背景CSS")
            else:
                print("❌ base.html未引入背景CSS")
    
    print("\n测试完成！")
    print("现在可以启动Flask应用并访问任意机体详情页查看背景效果。")
    
    return True

if __name__ == '__main__':
    test_background_system() 