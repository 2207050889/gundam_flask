#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from pathlib import Path

def check_gundam_details():
    """检查机体的详细数据"""
    db_path = Path('./instance/gundam.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 检查几个关键机体的数据
    test_gundams = [
        'RX-78-2 高达',
        'MSZ-006 Z高达', 
        'RX-0 独角兽高达',
        'MSN-04 沙扎比',
        'ZGMF-X10A 自由高达'
    ]
    
    print("="*80)
    print("机体详细数据检查")
    print("="*80)
    
    cursor.execute('''
        SELECT name, series, year, height, weight, pilot 
        FROM gundam 
        WHERE name IN ({})
        ORDER BY name
    '''.format(','.join('?' * len(test_gundams))), test_gundams)
    
    results = cursor.fetchall()
    
    for name, series, year, height, weight, pilot in results:
        print(f"\n机体名称: {name}")
        print(f"  系列: {series}")
        print(f"  年代: {year}")
        print(f"  身高: {height}m" if height else "  身高: 无数据")
        print(f"  体重: {weight}t" if weight else "  体重: 无数据") 
        print(f"  驾驶员: {pilot}" if pilot else "  驾驶员: 无数据")
        
        # 检查问题
        issues = []
        if not height:
            issues.append("缺少身高数据")
        if not weight:
            issues.append("缺少体重数据")
        if not pilot:
            issues.append("缺少驾驶员数据")
            
        if issues:
            print(f"  ⚠️  问题: {', '.join(issues)}")
        else:
            print(f"  ✅  数据完整")
    
    conn.close()
    print(f"\n检查完成！")

if __name__ == '__main__':
    check_gundam_details() 