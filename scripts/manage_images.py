import sys
import os

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from app import create_app, db
from app.models import Gundam

app = create_app()

def update_image_urls():
    """更新机体的不同类型图片URL"""
    
    # 定义不同类型的图片URL
    image_data = {
        # UC纪元系列
        'RX-78-2 高达': {
            'thumbnail': 'https://patchwiki.biligame.com/images/gundam/thumb/b/b3/s054e54usz0d9mdtm0cc54oe68if63c.jpg/200px-thumbnail.jpg',
            'detail': 'https://patchwiki.biligame.com/images/gundam/b/b3/s054e54usz0d9mdtm0cc54oe68if63c.jpg',
            'background': '/static/images/backgrounds/rx78_bg.jpg'
        },
        'MSZ-006 Z高达': {
            'thumbnail': 'https://patchwiki.biligame.com/images/gundam/thumb/2/2c/fetakbfqd3yjery92wsz26bdx9g2xe3.jpg/200px-thumbnail.jpg',
            'detail': 'https://patchwiki.biligame.com/images/gundam/2/2c/fetakbfqd3yjery92wsz26bdx9g2xe3.jpg',
            'background': '/static/images/backgrounds/zeta_bg.jpg'
        },
        'RX-0 独角兽高达': {
            'thumbnail': 'https://patchwiki.biligame.com/images/gundam/thumb/7/7f/ipzah2aqs0ad4r1790le6u5at2wl313.jpg/200px-thumbnail.jpg',
            'detail': 'https://patchwiki.biligame.com/images/gundam/7/7f/ipzah2aqs0ad4r1790le6u5at2wl313.jpg',
            'background': '/static/images/backgrounds/unicorn_bg.jpg'
        },
        'MSN-04 沙扎比': {
            'thumbnail': 'https://patchwiki.biligame.com/images/gundam/thumb/1/1e/5mmlcx0eaurqmdygro6l1ooad1beps4.jpg/200px-thumbnail.jpg',
            'detail': 'https://patchwiki.biligame.com/images/gundam/1/1e/5mmlcx0eaurqmdygro6l1ooad1beps4.jpg',
            'background': '/static/images/backgrounds/sazabi_bg.jpg'
        },
        
        # SEED系列
        'ZGMF-X10A 自由高达': {
            'thumbnail': 'https://patchwiki.biligame.com/images/gundam/thumb/7/78/g6f7ush4gl7nn9mrcf6jpxmdyuo2iyx.jpg/200px-thumbnail.jpg',
            'detail': 'https://patchwiki.biligame.com/images/gundam/7/78/g6f7ush4gl7nn9mrcf6jpxmdyuo2iyx.jpg',
            'background': '/static/images/backgrounds/freedom_bg.jpg'
        },
        'ZGMF-X20A 强袭自由高达': {
            'thumbnail': 'https://patchwiki.biligame.com/images/gundam/thumb/8/84/d9jw2ee86e25bzm54enrayqmh0vsunu.jpg/200px-thumbnail.jpg',
            'detail': 'https://patchwiki.biligame.com/images/gundam/8/84/d9jw2ee86e25bzm54enrayqmh0vsunu.jpg',
            'background': '/static/images/backgrounds/strike_freedom_bg.jpg'
        },
        'MBF-P02 异端高达红色机': {
            'thumbnail': 'https://patchwiki.biligame.com/images/gundam/thumb/c/cd/mg5607rqup0lcm8h3o40vynhf9tmcru.jpg/200px-thumbnail.jpg',
            'detail': 'https://patchwiki.biligame.com/images/gundam/c/cd/mg5607rqup0lcm8h3o40vynhf9tmcru.jpg',
            'background': '/static/images/backgrounds/astray_red_bg.jpg'
        },
        'GAT-X105 强袭高达': {
            'thumbnail': 'https://patchwiki.biligame.com/images/gundam/thumb/a/ae/i6zeorcfycxhsey9de6msk8frjwir1z.jpg/200px-thumbnail.jpg',
            'detail': 'https://patchwiki.biligame.com/images/gundam/a/ae/i6zeorcfycxhsey9de6msk8frjwir1z.jpg',
            'background': '/static/images/backgrounds/strike_bg.jpg'
        },
        
        # 00系列
        'GN-001 能天使高达': {
            'thumbnail': 'https://patchwiki.biligame.com/images/gundam/thumb/b/b2/omeeu07rfxa7jutjvqg3mh50ydiywen.jpg/200px-thumbnail.jpg',
            'detail': 'https://patchwiki.biligame.com/images/gundam/b/b2/omeeu07rfxa7jutjvqg3mh50ydiywen.jpg',
            'background': '/static/images/backgrounds/exia_bg.jpg'
        },
        'GN-0000 00高达': {
            'thumbnail': 'https://patchwiki.biligame.com/images/gundam/thumb/b/b8/t8fnknwalliranamsp6kh7nle150xu9.jpg/200px-thumbnail.jpg',
            'detail': 'https://patchwiki.biligame.com/images/gundam/b/b8/t8fnknwalliranamsp6kh7nle150xu9.jpg',
            'background': '/static/images/backgrounds/00_bg.jpg'
        },
        'GN-002 力天使高达': {
            'thumbnail': 'https://patchwiki.biligame.com/images/gundam/thumb/8/89/ciki99558djuzzmqwsje5wdf3d1qpx2.jpg/200px-thumbnail.jpg',
            'detail': 'https://patchwiki.biligame.com/images/gundam/8/89/ciki99558djuzzmqwsje5wdf3d1qpx2.jpg',
            'background': '/static/images/backgrounds/dynames_bg.jpg'
        },
        
        # W系列
        'XXXG-00W0 飞翼零式高达': {
            'thumbnail': 'https://patchwiki.biligame.com/images/gundam/thumb/b/b1/fa0kiq7pj1ify2lteg1j3wptz7i0gdg.jpg/200px-thumbnail.jpg',
            'detail': 'https://patchwiki.biligame.com/images/gundam/b/b1/fa0kiq7pj1ify2lteg1j3wptz7i0gdg.jpg',
            'background': '/static/images/backgrounds/wing_zero_bg.jpg'
        },
        'XXXG-01W 飞翼高达': {
            'thumbnail': 'https://patchwiki.biligame.com/images/gundam/thumb/d/df/pxaru59domboljv3hz635toux05cz0n.jpg/200px-thumbnail.jpg',
            'detail': 'https://patchwiki.biligame.com/images/gundam/d/df/pxaru59domboljv3hz635toux05cz0n.jpg',
            'background': '/static/images/backgrounds/wing_bg.jpg'
        },
        
        # 铁血系列
        'ASW-G-08 高达巴巴托斯': {
            'thumbnail': 'https://patchwiki.biligame.com/images/gundam/thumb/c/c2/o1gsyioepbzfrh62nnejg9mm54xzhtm.jpg/200px-thumbnail.jpg',
            'detail': 'https://patchwiki.biligame.com/images/gundam/c/c2/o1gsyioepbzfrh62nnejg9mm54xzhtm.jpg',
            'background': '/static/images/backgrounds/barbatos_bg.jpg'
        },
        
        # 新增UC纪元机体
        'RX-93ν高达': {
            'thumbnail': '/static/images/thumbnails/nu_gundam_thumb.jpg',
            'detail': '/static/images/details/nu_gundam_detail.jpg',
            'background': '/static/images/backgrounds/nu_gundam_bg.jpg'
        },
        'MSN-06S新安洲': {
            'thumbnail': '/static/images/thumbnails/sinanju_thumb.jpg',
            'detail': '/static/images/details/sinanju_detail.jpg',
            'background': '/static/images/backgrounds/sinanju_bg.jpg'
        },
        'RX-93-ν2Hi-ν高达': {
            'thumbnail': '/static/images/thumbnails/hi_nu_thumb.jpg',
            'detail': '/static/images/details/hi_nu_detail.jpg',
            'background': '/static/images/backgrounds/hi_nu_bg.jpg'
        },
        'MSN-04-2夜莺': {
            'thumbnail': '/static/images/thumbnails/nightingale_thumb.jpg',
            'detail': '/static/images/details/nightingale_detail.jpg',
            'background': '/static/images/backgrounds/nightingale_bg.jpg'
        },
        'RX-0独角兽高达2号机报丧女妖': {
            'thumbnail': '/static/images/thumbnails/banshee_thumb.jpg',
            'detail': '/static/images/details/banshee_detail.jpg',
            'background': '/static/images/backgrounds/banshee_bg.jpg'
        },
        'RX-0独角兽高达3号机凤凰': {
            'thumbnail': '/static/images/thumbnails/phenex_thumb.jpg',
            'detail': '/static/images/details/phenex_detail.jpg',
            'background': '/static/images/backgrounds/phenex_bg.jpg'
        },
        
        # 新增SEED系列机体
        'MBF-02强袭嫣红': {
            'thumbnail': '/static/images/thumbnails/rouge_thumb.jpg',
            'detail': '/static/images/details/rouge_detail.jpg',
            'background': '/static/images/backgrounds/rouge_bg.jpg'
        }
    }
    
    with app.app_context():
        print("开始更新机体图片URL...")
        print("=" * 60)
        
        updated_count = 0
        
        for gundam in Gundam.query.all():
            if gundam.name in image_data:
                data = image_data[gundam.name]
                
                # 更新不同类型的图片URL
                old_thumbnail = getattr(gundam, 'thumbnail_url', None)
                old_detail = getattr(gundam, 'detail_image_url', None)
                old_background = getattr(gundam, 'background_url', None)
                
                # 如果字段不存在，先设置为None
                if not hasattr(gundam, 'thumbnail_url'):
                    gundam.thumbnail_url = None
                if not hasattr(gundam, 'detail_image_url'):
                    gundam.detail_image_url = None
                if not hasattr(gundam, 'background_url'):
                    gundam.background_url = None
                
                # 更新图片URL
                gundam.thumbnail_url = data['thumbnail']
                gundam.detail_image_url = data['detail']
                gundam.background_url = data['background']
                
                # 保持原有的image_url作为兼容性
                gundam.image_url = data['detail']
                
                print(f"✅ 更新 {gundam.name}:")
                print(f"   缩略图: {old_thumbnail} -> {data['thumbnail']}")
                print(f"   详情图: {old_detail} -> {data['detail']}")
                print(f"   背景图: {old_background} -> {data['background']}")
                print()
                
                updated_count += 1
            else:
                print(f"⚠️ 未找到 {gundam.name} 的图片配置")
        
        if updated_count > 0:
            db.session.commit()
            print(f"✅ 成功更新 {updated_count} 个机体的图片URL")
        else:
            print("❌ 没有更新任何图片URL")

def check_image_status():
    """检查所有机体的图片状态"""
    with app.app_context():
        gundams = Gundam.query.all()
        
        print("=== 机体图片状态检查 ===")
        print(f"总共 {len(gundams)} 个机体")
        print("=" * 80)
        
        for gundam in gundams:
            thumbnail = getattr(gundam, 'thumbnail_url', None)
            detail = getattr(gundam, 'detail_image_url', None)
            background = getattr(gundam, 'background_url', None)
            
            status = []
            if thumbnail: status.append("缩略图✅")
            else: status.append("缩略图❌")
            
            if detail: status.append("详情图✅")
            else: status.append("详情图❌")
            
            if background: status.append("背景图✅")
            else: status.append("背景图❌")
            
            print(f"{gundam.name:<30} | {' | '.join(status)}")

def interactive_image_manager():
    """交互式图片管理"""
    print("=== 高达图片管理工具 ===")
    print("1. 更新所有图片URL")
    print("2. 检查图片状态")
    print("3. 添加图片字段到数据库")
    print("0. 退出")
    
    while True:
        choice = input("\n请选择操作 (0-3): ").strip()
        
        if choice == '0':
            print("退出图片管理工具")
            break
        elif choice == '1':
            update_image_urls()
        elif choice == '2':
            check_image_status()
        elif choice == '3':
            # 这里需要手动添加字段，因为SQLAlchemy模型还没更新
            print("请先运行: python scripts/add_image_fields.py")
        else:
            print("❌ 无效选择，请重新输入")

if __name__ == "__main__":
    interactive_image_manager() 