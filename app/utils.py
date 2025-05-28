"""
工具函数模块，提供所有路由共用的功能
"""
import os
from flask import current_app, url_for

def is_absolute_url(url):
    """检查URL是否为绝对URL"""
    if not url:
        return False
    return url.startswith('http://') or url.startswith('https://')

def file_exists_in_static(relative_path):
    """检查文件是否存在于静态目录"""
    if not relative_path:
        return False
    
    # 确保路径分隔符正确
    relative_path = relative_path.replace('/', os.path.sep)
    
    # 构建完整路径
    full_path = os.path.normpath(os.path.join(current_app.static_folder, relative_path))
    
    # 检查文件是否存在
    exists = os.path.exists(full_path)
    if exists:
        print(f"文件存在: {relative_path} -> {full_path}")
    else:
        print(f"文件不存在: {relative_path} -> {full_path}")
    
    return exists

def get_placeholder_path():
    """获取备用的占位图片路径"""
    placeholder_img = 'images/placeholder_image.png'
    
    # 优先使用placeholder_image.png，如果存在
    if file_exists_in_static(placeholder_img):
        return placeholder_img
    else:
        return None

def process_gundam_image(gundam):
    """处理高达机体的图片URL，返回处理后的图片URL和标志
    
    Args:
        gundam: 高达机体对象
        
    Returns:
        tuple: (primary_image, is_absolute_url_flag)
            primary_image: 主图片URL或路径
            is_absolute_url_flag: 是否为绝对URL的标志
    """
    # 如果image_url是完整URL，直接使用
    if is_absolute_url(gundam.image_url):
        return gundam.image_url, True
    
    # 使用占位符图片
    placeholder = get_placeholder_path()
    if placeholder:
        return placeholder, False
    
    # 没有找到任何有效图片
    return '', False

def prepare_gundam_for_view(gundam):
    """为视图准备高达机体，添加图片URL属性
    
    Args:
        gundam: 高达机体对象
        
    Returns:
        gundam: 添加了图片属性的同一对象
    """
    primary_image, is_absolute_url_flag = process_gundam_image(gundam)
    gundam.primary_image = primary_image
    gundam.is_absolute_url = is_absolute_url_flag
    return gundam

def prepare_gundams_for_view(gundams):
    """为视图准备多个高达机体，添加图片URL属性
    
    Args:
        gundams: 高达机体对象列表
        
    Returns:
        gundams: 添加了图片属性的同一对象列表
    """
    for gundam in gundams:
        prepare_gundam_for_view(gundam)
    return gundams 