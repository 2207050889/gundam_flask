import sys
import os

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from app import create_app, db
from app.models import Gundam

app = create_app()

# 为每个机体定义简洁介绍
BRIEF_INTROS = {
    # UC纪元系列
    'RX-78-2高达': '联邦军开发的第一台实用型高达，阿姆罗·雷的座机，开启了高达传说。',
    'MSZ-006Z高达': '奥古开发的可变型MS,格利普斯战役的主角机体,具备MS和MA双重形态。',
    'RX-0独角兽高达': '搭载精神感应框架的白色独角兽，拉普拉斯之盒的钥匙。',
    'MSN-04沙扎比': '夏亚专用的新吉翁军旗舰级MS,搭载浮游炮系统的红色彗星最终座机。',
    'RX-93ν高达': '阿姆罗设计的最终高达，搭载精神感应框架，与沙扎比决战的传奇机体。',
    'MSN-06S新安洲': '弗尔·伏朗托的专用机,新吉翁军的最新锐MS,拥有压倒性的性能。',
    'MSN-04-2夜莺': '夏亚的巨大MA,沙扎比的后继机，拥有更强大的火力和防护。',
    'RX-0独角兽高达2号机·报丧女妖': '黑色的独角兽，马里达的座机，背负着悲伤命运的机体。',
    'RX-0独角兽高达3号机·菲尼克斯': '金色的独角兽，传说中的第三台机体，拥有神秘的力量。',
    
    # SEED系列
    'ZGMF-X10A自由高达': '基拉专用的核动力高达，搭载多重锁定系统，象征着自由的翅膀。',
    'ZGMF-X20A强袭自由高达': '自由高达的后继机，基拉的最终座机，拥有更强的火力和机动性。',
    'MBF-P02异端高达红色机': '红色的异端高达，搭载战术刀的近战特化机体。',
    'GAT-X105强袭高达': '地球联合军的试作型高达，基拉的初始座机。',
    'MBF-02强袭嫣红': '强袭高达的改良型，搭载了更先进的武装系统。',
    'ORB-01拂晓高达': '拂晓高达是在奥布联合首长国首长乌兹米·尤拉·阿斯哈命令下奥布“曙光社”秘密开发完成。',
    'ZGMF-X19A无限正义高达': '阿斯兰的座机，搭载多重锁定系统，象征着正义的翅膀。',
    'ZGMF/A-262B强袭自由高达二式': '基拉的最终座机，拥有更强的火力和机动性。',
    'ZGMF/A-262PD-P非凡强袭自由高达': '由「强袭自由高达」改修升级而来的「强袭自由高达二式」装备了新设计的「荣耀捍卫者」后的姿态。',
    
    # 00系列
    'GN-001 能天使高达': '刹那的座机,天人组织的第一代高达,搭载GN粒子驱动系统。',
    'GN-0000 00高达': '双重驱动系统的革新机体，刹那的最终座机。',
    'GN-002力天使高达': '洛克昂的狙击型高达，擅长远距离精密射击。',
    'GN-003主天使高达': '主天使高达,「天人武装组织」所拥有的高达之一,搭载「GN太阳炉」，拥有近乎无限的能源和惊人的机动性。',
    'GN-005德天使高达': '搭载GN-Drive,拥有近乎无限的能源和惊人的机动性。',
    'GN-006智天使高达': '特化了远距离射击战的高达。Dynames高达的发展机。',
    
    # W系列
    'XXXG-00W0飞翼零式高达': '希罗的最强座机，搭载零式系统的天使般机体。',
    'XXXG-01W飞翼高达': '希罗的初始座机，拥有鸟型变形能力的高达。',
    'XXXG-00W0飞翼零式高达EW': '飞翼零式高达EW是G系列的设计原型机体,装备有突入大气层用的双联装甲护翼。',
    
    # 铁血系列
    'ASW-G-08 高达巴巴托斯': '三日月的座机,72柱魔神之一,拥有野兽般的战斗本能。',
    'ASW-G-08高达巴巴托斯·天狼座': '巴巴托斯·天狼座是巴巴托斯·天狼座帝王形态的量产型，装备了新设计的「荣耀捍卫者」后的姿态。',
    'ASW-G-08高达巴巴托斯·天狼座帝王形态': '在火星都市“克里塞”近郊和MA——“哈斯蒙”展开激战的“巴巴托斯天狼型”在赢得胜利的同时，也跟驾驶员三日月·奥古斯一样陷入满身疮痍的状态。',
}

def update_brief_intros():
    """为所有机体更新简洁介绍"""
    with app.app_context():
        print("开始更新机体简洁介绍...")
        print("=" * 60)
        
        updated_count = 0
        
        for gundam in Gundam.query.all():
            if gundam.name in BRIEF_INTROS:
                old_intro = gundam.brief_intro
                gundam.brief_intro = BRIEF_INTROS[gundam.name]
                
                print(f"✅ 更新 {gundam.name}:")
                print(f"   旧简介: {old_intro[:50] if old_intro else 'None'}...")
                print(f"   新简介: {gundam.brief_intro}")
                print()
                
                updated_count += 1
            else:
                print(f"⚠️ 未找到 {gundam.name} 的简介配置")
        
        if updated_count > 0:
            db.session.commit()
            print(f"✅ 成功更新 {updated_count} 个机体的简洁介绍")
        else:
            print("❌ 没有更新任何简洁介绍")

if __name__ == "__main__":
    update_brief_intros() 