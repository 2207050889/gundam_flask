import sys
import os

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from app import create_app, db
from app.models import Gundam

app = create_app()

def list_all_gundams():
    """列出所有机体"""
    with app.app_context():
        gundams = Gundam.query.all()
        print(f"当前数据库中有 {len(gundams)} 个机体:")
        print("=" * 80)
        print(f"{'ID':>3} | {'机体名称':<25} | {'系列':<10} | {'年代':<6} | {'驾驶员':<15}")
        print("-" * 80)
        
        for g in gundams:
            print(f"{g.id:>3} | {g.name:<25} | {g.series:<10} | {g.year or '未知':<6} | {g.pilot or '未知':<15}")
        
        print("=" * 80)
        
        # 按系列统计
        series_count = {}
        for g in gundams:
            series_count[g.series] = series_count.get(g.series, 0) + 1
        
        print("\n系列统计:")
        for series, count in series_count.items():
            print(f"  {series}: {count} 个机体")

if __name__ == "__main__":
    print("=" * 50)
    print("高达数据库 - 机体列表")
    print("=" * 50)
    list_all_gundams() 