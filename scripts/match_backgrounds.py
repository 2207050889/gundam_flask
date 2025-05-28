#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sqlite3
from pathlib import Path

def get_gundam_list():
    """从数据库获取机体列表"""
    db_path = Path('./instance/gundam.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, name FROM gundam ORDER BY id')
    gundams = cursor.fetchall()
    
    conn.close()
    return gundams

def get_image_files():
    """获取已上传的图片文件列表"""
    images_dir = Path('./app/static/images/details')
    if not images_dir.exists():
        return []
    
    image_files = []
    for file in images_dir.glob('*.jpg'):
        image_files.append(file.name)
    
    return sorted(image_files)

def match_names():
    """匹配机体名称和图片文件"""
    gundams = get_gundam_list()
    images = get_image_files()
    
    print("="*80)
    print("机体背景图片匹配分析")
    print("="*80)
    
    print(f"\n数据库中的机体数量: {len(gundams)}")
    print(f"上传的图片数量: {len(images)}")
    
    print("\n机体名称与图片文件匹配:")
    print("-"*80)
    
    matches = {}
    unmatched_gundams = []
    unmatched_images = list(images)
    
    # 手动匹配特殊情况
    special_matches = {
        'RX-0独角兽高达2号机·报丧女妖': 'RX-0独角兽高达2号机.jpg',
        'RX-0独角兽高达3号机·菲尼克斯': 'RX-0独角兽高达3号机.jpg',
        'ASW-G-08高达巴巴托斯·天狼座': 'ASW-G-08高达巴巴托斯·天狼座.jpg',
        'ASW-G-08高达巴巴托斯·天狼座帝王形态': 'ASW-G-08高达巴巴托斯·天狼座帝王形态.jpg',
        'XXXG-00W0飞翼零式高达EW': 'XXXG-00W0飞翼零式高达EW.jpg'
    }
    
    for gundam_id, gundam_name in gundams:
        matched = False
        best_match = None
        
        # 首先检查特殊匹配
        if gundam_name in special_matches:
            image_file = special_matches[gundam_name]
            if image_file in images:
                matches[gundam_name] = image_file
                if image_file in unmatched_images:
                    unmatched_images.remove(image_file)
                matched = True
                best_match = image_file
        
        # 如果没有特殊匹配，尝试精确匹配
        if not matched:
            for image in images:
                if image in unmatched_images:  # 只匹配未使用的图片
                    image_name = image.replace('.jpg', '')
                    if image_name in gundam_name or gundam_name.replace(' ', '') in image_name.replace(' ', ''):
                        matches[gundam_name] = image
                        unmatched_images.remove(image)
                        matched = True
                        best_match = image
                        break
        
        # 如果还没有匹配，尝试部分匹配
        if not matched:
            for image in images:
                if image in unmatched_images:  # 只匹配未使用的图片
                    image_name = image.replace('.jpg', '')
                    # 提取关键词进行匹配
                    gundam_keywords = gundam_name.replace(' ', '').replace('·', '').replace('-', '')
                    image_keywords = image_name.replace(' ', '').replace('·', '').replace('-', '')
                    
                    if any(keyword in image_keywords for keyword in gundam_keywords.split('高达')[0:1] if keyword):
                        if not best_match:
                            best_match = image
                            matches[gundam_name] = image
                            unmatched_images.remove(image)
                            matched = True
                            break
        
        if best_match:
            print(f"✓ {gundam_name:<35} -> {best_match}")
        else:
            unmatched_gundams.append(gundam_name)
            print(f"✗ {gundam_name:<35} -> 未找到匹配")
    
    if unmatched_gundams:
        print(f"\n未匹配的机体 ({len(unmatched_gundams)}):")
        for gundam in unmatched_gundams:
            print(f"  - {gundam}")
    
    if unmatched_images:
        print(f"\n未使用的图片 ({len(unmatched_images)}):")
        for image in unmatched_images:
            print(f"  - {image}")
    
    return matches, gundams

def generate_css_classes(matches, gundams):
    """生成CSS背景类"""
    css_content = "\n/* 机体详情页背景 - 自动生成 */\n"
    
    for gundam_id, gundam_name in gundams:
        # 生成CSS类名
        css_class = gundam_name.lower()
        css_class = css_class.replace(' ', '-').replace('·', '-').replace('/', '-')
        css_class = css_class.replace('高达', 'gundam').replace('扎古', 'zaku').replace('沙扎比', 'sazabi')
        css_class = 'bg-' + css_class
        
        if gundam_name in matches:
            image_file = matches[gundam_name]
            css_content += f"body.detail-page.{css_class}::before {{\n"
            css_content += f"    background-image: url('../images/details/{image_file}');\n"
            css_content += f"}}\n\n"
        else:
            css_content += f"/* {css_class}: 缺少图片 {gundam_name} */\n"
    
    return css_content

def generate_template_logic(gundams):
    """生成模板逻辑"""
    template_content = "{% set bg_class = 'bg-default' %}\n"
    
    for gundam_id, gundam_name in gundams:
        css_class = gundam_name.lower()
        css_class = css_class.replace(' ', '-').replace('·', '-').replace('/', '-')
        css_class = css_class.replace('高达', 'gundam').replace('扎古', 'zaku').replace('沙扎比', 'sazabi')
        css_class = 'bg-' + css_class
        
        template_content += "{% elif gundam.name == '" + gundam_name + "' %}\n"
        template_content += "    {% set bg_class = '" + css_class + "' %}\n"
    
    return template_content

if __name__ == '__main__':
    matches, gundams = match_names()
    
    # 生成CSS
    css_content = generate_css_classes(matches, gundams)
    with open('generated_backgrounds.css', 'w', encoding='utf-8') as f:
        f.write(css_content)
    
    # 生成模板逻辑
    template_content = generate_template_logic(gundams)
    with open('generated_template_logic.txt', 'w', encoding='utf-8') as f:
        f.write(template_content)
    
    print(f"\n已生成:")
    print(f"  - generated_backgrounds.css (CSS背景类)")
    print(f"  - generated_template_logic.txt (模板逻辑)")
    print(f"\n匹配成功率: {len(matches)}/{len(gundams)} ({len(matches)/len(gundams)*100:.1f}%)") 