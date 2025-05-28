import sys
import os

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from app import create_app, db
from app.models import Gundam

app = create_app()

def delete_by_id(gundam_id):
    """根据ID删除机体"""
    with app.app_context():
        gundam = Gundam.query.get(gundam_id)
        if gundam:
            print(f"删除机体: ID={gundam.id}, 名称={gundam.name}")
            db.session.delete(gundam)
            db.session.commit()
            print("✅ 删除成功")
            return True
        else:
            print(f"❌ 未找到ID为 {gundam_id} 的机体")
            return False

def delete_by_name(gundam_name):
    """根据完整名称删除机体"""
    with app.app_context():
        gundam = Gundam.query.filter_by(name=gundam_name).first()
        if gundam:
            print(f"删除机体: ID={gundam.id}, 名称={gundam.name}")
            db.session.delete(gundam)
            db.session.commit()
            print("✅ 删除成功")
            return True
        else:
            print(f"❌ 未找到名称为 '{gundam_name}' 的机体")
            return False

def delete_by_keyword(keyword):
    """根据关键词删除所有匹配的机体"""
    with app.app_context():
        gundams = Gundam.query.filter(Gundam.name.contains(keyword)).all()
        if gundams:
            print(f"找到 {len(gundams)} 个包含关键词 '{keyword}' 的机体:")
            for gundam in gundams:
                print(f"  - ID={gundam.id}, 名称={gundam.name}")
            
            confirm = input("确认删除以上所有机体吗？(y/N): ").strip().lower()
            if confirm == 'y':
                for gundam in gundams:
                    print(f"删除: {gundam.name}")
                    db.session.delete(gundam)
                db.session.commit()
                print(f"✅ 成功删除 {len(gundams)} 个机体")
                return True
            else:
                print("❌ 取消删除")
                return False
        else:
            print(f"❌ 未找到包含关键词 '{keyword}' 的机体")
            return False

def delete_by_series(series_name):
    """根据系列删除所有机体"""
    with app.app_context():
        gundams = Gundam.query.filter_by(series=series_name).all()
        if gundams:
            print(f"找到 {len(gundams)} 个属于 '{series_name}' 系列的机体:")
            for gundam in gundams:
                print(f"  - ID={gundam.id}, 名称={gundam.name}")
            
            confirm = input(f"确认删除 '{series_name}' 系列的所有机体吗？(y/N): ").strip().lower()
            if confirm == 'y':
                for gundam in gundams:
                    print(f"删除: {gundam.name}")
                    db.session.delete(gundam)
                db.session.commit()
                print(f"✅ 成功删除 {len(gundams)} 个机体")
                return True
            else:
                print("❌ 取消删除")
                return False
        else:
            print(f"❌ 未找到属于 '{series_name}' 系列的机体")
            return False

def interactive_delete():
    """交互式删除"""
    with app.app_context():
        print("=== 交互式机体删除工具 ===")
        print("1. 根据ID删除")
        print("2. 根据完整名称删除")
        print("3. 根据关键词删除")
        print("4. 根据系列删除")
        print("5. 查看所有机体")
        print("0. 退出")
        
        while True:
            choice = input("\n请选择操作 (0-5): ").strip()
            
            if choice == '0':
                print("退出删除工具")
                break
            elif choice == '1':
                try:
                    gundam_id = int(input("请输入机体ID: "))
                    delete_by_id(gundam_id)
                except ValueError:
                    print("❌ 请输入有效的数字ID")
            elif choice == '2':
                gundam_name = input("请输入完整机体名称: ").strip()
                if gundam_name:
                    delete_by_name(gundam_name)
            elif choice == '3':
                keyword = input("请输入关键词: ").strip()
                if keyword:
                    delete_by_keyword(keyword)
            elif choice == '4':
                series_name = input("请输入系列名称 (UC纪元/SEED系列/00系列/W系列/铁血系列): ").strip()
                if series_name:
                    delete_by_series(series_name)
            elif choice == '5':
                # 显示所有机体
                gundams = Gundam.query.all()
                print(f"\n当前数据库中有 {len(gundams)} 个机体:")
                print("-" * 60)
                for g in gundams:
                    print(f"ID={g.id:>2} | {g.name:<25} | {g.series}")
                print("-" * 60)
            else:
                print("❌ 无效选择，请重新输入")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 命令行模式
        action = sys.argv[1]
        if action == "id" and len(sys.argv) > 2:
            delete_by_id(int(sys.argv[2]))
        elif action == "name" and len(sys.argv) > 2:
            delete_by_name(sys.argv[2])
        elif action == "keyword" and len(sys.argv) > 2:
            delete_by_keyword(sys.argv[2])
        elif action == "series" and len(sys.argv) > 2:
            delete_by_series(sys.argv[2])
        else:
            print("用法:")
            print("  python scripts/delete_gundam.py id <机体ID>")
            print("  python scripts/delete_gundam.py name <完整机体名称>")
            print("  python scripts/delete_gundam.py keyword <关键词>")
            print("  python scripts/delete_gundam.py series <系列名称>")
    else:
        # 交互式模式
        interactive_delete() 