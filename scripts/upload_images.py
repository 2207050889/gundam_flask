import os
import shutil
from pathlib import Path

def create_image_directories():
    """创建图片目录结构"""
    base_path = Path("app/static/images")
    
    directories = [
        "thumbnails",
        "details", 
        "backgrounds"
    ]
    
    for dir_name in directories:
        dir_path = base_path / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✅ 创建目录: {dir_path}")

def get_machine_mapping():
    """获取机体名称映射"""
    return {
        # UC纪元系列
        "RX-93ν高达": "nu_gundam",
        "MSN-06S新安洲": "sinanju", 
        "RX-93-ν2Hi-ν高达": "hi_nu",
        "MSN-04-2夜莺": "nightingale",
        "RX-0独角兽高达2号机报丧女妖": "banshee",
        "RX-0独角兽高达3号机凤凰": "phenex",
        
        # SEED系列
        "MBF-02强袭嫣红": "rouge",
        
        # 可以继续添加其他机体
        "RX-78-2 高达": "rx78_2",
        "MSZ-006 Z高达": "zeta",
        "RX-0 独角兽高达": "unicorn",
        "MSN-04 沙扎比": "sazabi",
        "ZGMF-X10A 自由高达": "freedom",
        "ZGMF-X20A 强袭自由高达": "strike_freedom",
        "GN-001 能天使高达": "exia",
        "GN-0000 00高达": "double_o",
        "XXXG-00W0 飞翼零式高达": "wing_zero",
        "ASW-G-08 高达巴巴托斯": "barbatos"
    }

def upload_single_image():
    """单个图片上传"""
    print("=== 单个图片上传 ===")
    
    # 显示机体列表
    mapping = get_machine_mapping()
    print("\n可用机体列表:")
    for i, (chinese_name, english_name) in enumerate(mapping.items(), 1):
        print(f"{i:2d}. {chinese_name} ({english_name})")
    
    # 选择机体
    try:
        choice = int(input("\n请选择机体编号: ")) - 1
        chinese_name = list(mapping.keys())[choice]
        english_name = mapping[chinese_name]
    except (ValueError, IndexError):
        print("❌ 无效选择")
        return
    
    # 选择图片类型
    print(f"\n为 {chinese_name} 选择图片类型:")
    print("1. 缩略图 (thumbnails)")
    print("2. 详情图 (details)")
    print("3. 背景图 (backgrounds)")
    
    type_mapping = {
        "1": ("thumbnails", "_thumb.jpg"),
        "2": ("details", "_detail.jpg"), 
        "3": ("backgrounds", "_bg.jpg")
    }
    
    img_type = input("请选择图片类型 (1-3): ")
    if img_type not in type_mapping:
        print("❌ 无效选择")
        return
    
    folder, suffix = type_mapping[img_type]
    
    # 输入源文件路径
    source_path = input("请输入图片文件完整路径: ").strip('"')
    if not os.path.exists(source_path):
        print("❌ 文件不存在")
        return
    
    # 生成目标路径
    target_filename = f"{english_name}{suffix}"
    target_path = f"app/static/images/{folder}/{target_filename}"
    
    # 复制文件
    try:
        shutil.copy2(source_path, target_path)
        print(f"✅ 成功上传: {target_path}")
    except Exception as e:
        print(f"❌ 上传失败: {e}")

def batch_upload_images():
    """批量图片上传"""
    print("=== 批量图片上传 ===")
    print("请将图片文件放在一个文件夹中，按以下命名规范:")
    print("- {机体英文名}_thumb.jpg (缩略图)")
    print("- {机体英文名}_detail.jpg (详情图)")
    print("- {机体英文名}_bg.jpg (背景图)")
    print("\n例如: nu_gundam_thumb.jpg, nu_gundam_detail.jpg, nu_gundam_bg.jpg")
    
    source_dir = input("\n请输入包含图片的文件夹路径: ").strip('"')
    if not os.path.exists(source_dir):
        print("❌ 文件夹不存在")
        return
    
    # 扫描文件
    uploaded_count = 0
    for filename in os.listdir(source_dir):
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue
            
        source_path = os.path.join(source_dir, filename)
        
        # 判断图片类型
        if '_thumb.' in filename:
            target_dir = "app/static/images/thumbnails"
        elif '_detail.' in filename:
            target_dir = "app/static/images/details"
        elif '_bg.' in filename:
            target_dir = "app/static/images/backgrounds"
        else:
            print(f"⚠️ 跳过未识别格式: {filename}")
            continue
        
        # 复制文件
        target_path = os.path.join(target_dir, filename)
        try:
            shutil.copy2(source_path, target_path)
            print(f"✅ 上传: {filename} -> {target_path}")
            uploaded_count += 1
        except Exception as e:
            print(f"❌ 上传失败 {filename}: {e}")
    
    print(f"\n✅ 批量上传完成，共处理 {uploaded_count} 个文件")

def list_current_images():
    """列出当前图片状态"""
    print("=== 当前图片状态 ===")
    
    base_path = Path("app/static/images")
    folders = ["thumbnails", "details", "backgrounds"]
    
    for folder in folders:
        folder_path = base_path / folder
        print(f"\n📁 {folder}:")
        
        if folder_path.exists():
            files = list(folder_path.glob("*"))
            if files:
                for file in sorted(files):
                    size_kb = file.stat().st_size // 1024
                    print(f"   {file.name} ({size_kb}KB)")
            else:
                print("   (空)")
        else:
            print("   (目录不存在)")

def interactive_upload():
    """交互式图片上传工具"""
    create_image_directories()
    
    print("=== 高达图片上传工具 ===")
    print("1. 单个图片上传")
    print("2. 批量图片上传") 
    print("3. 查看当前图片状态")
    print("4. 显示命名规范")
    print("0. 退出")
    
    while True:
        choice = input("\n请选择操作 (0-4): ").strip()
        
        if choice == '0':
            print("退出图片上传工具")
            break
        elif choice == '1':
            upload_single_image()
        elif choice == '2':
            batch_upload_images()
        elif choice == '3':
            list_current_images()
        elif choice == '4':
            show_naming_convention()
        else:
            print("❌ 无效选择，请重新输入")

def show_naming_convention():
    """显示命名规范"""
    print("=== 图片命名规范 ===")
    
    mapping = get_machine_mapping()
    print("\n机体英文名对照表:")
    for chinese, english in mapping.items():
        print(f"{chinese:<25} -> {english}")
    
    print("\n文件命名格式:")
    print("- 缩略图: {英文名}_thumb.jpg")
    print("- 详情图: {英文名}_detail.jpg") 
    print("- 背景图: {英文名}_bg.jpg")
    
    print("\n示例:")
    print("- nu_gundam_thumb.jpg")
    print("- nu_gundam_detail.jpg")
    print("- nu_gundam_bg.jpg")

if __name__ == "__main__":
    interactive_upload() 