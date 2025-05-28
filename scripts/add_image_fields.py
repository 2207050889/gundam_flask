import sys
import os

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from app import create_app, db

app = create_app()

def add_image_fields():
    """为Gundam模型添加新的图片字段"""
    with app.app_context():
        # 添加新的图片字段
        try:
            # 检查字段是否已存在
            db.engine.execute("SELECT thumbnail_url FROM gundam LIMIT 1")
            print("✅ 图片字段已存在")
        except:
            # 添加新字段
            print("添加新的图片字段...")
            
            # 添加缩略图URL字段
            db.engine.execute("ALTER TABLE gundam ADD COLUMN thumbnail_url VARCHAR(200)")
            print("✅ 添加 thumbnail_url 字段")
            
            # 添加详情页大图URL字段  
            db.engine.execute("ALTER TABLE gundam ADD COLUMN detail_image_url VARCHAR(200)")
            print("✅ 添加 detail_image_url 字段")
            
            # 添加背景图URL字段
            db.engine.execute("ALTER TABLE gundam ADD COLUMN background_url VARCHAR(200)")
            print("✅ 添加 background_url 字段")
            
            print("✅ 所有图片字段添加完成")

if __name__ == "__main__":
    add_image_fields() 