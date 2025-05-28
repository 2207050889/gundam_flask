from app import create_app, db
from app.models import Gundam # Removed User, Comment as they are not directly initialized here

app = create_app()

# ==============================================================================
# TODO: 用户需要填充此列表！
# 这是您项目中所有高达机体的完整列表。
# 每个条目都是一个字典，至少需要 'name' 和 'series'。
# 其他字段如 'year', 'height', 'weight', 'pilot', 'description', 'image_url' 是可选的初始值。
# 您可以参考 gundam_flask/app/static/data/all_gundams.json 来获取机体名称，
# 但您需要为它们确定正确的 'series' 值 (如 'UC纪元', 'SEED系列' 等)。
# description 可以是简短的初始描述，后续会被爬虫更新。
# image_url 可以是本地占位符图片的路径。
# ==============================================================================
ALL_GUNDAM_DATA = [
    {
        'name': 'RX-78-2高达', 
        'series': 'UC纪元',  # 注意：这里可能需要根据您的系列分类进行调整
        'year': '0079',
        'height': 18.0,
        'weight': 43.4,
        'pilot': '阿姆罗·雷',
        'description': 'RX计划中开发的泛用性MS，V作战的核心。经历了一年战争的诸多著名战役，创造了辉煌的战果。',
        
    },
  
     {
         'name': 'MSZ-006Z高达', 
         'series': 'UC纪元', 
         'year': '0087',
         'height': 18.7,
         'weight': 28.7,
         'pilot': '卡缪·维丹',
         'description': '奥古开发的TMS（可变MS），格利普斯战役中卡缪·维丹的座机。',       
     },

     {
         'name': 'RX-0独角兽高达', 
         'series': 'UC纪元', 
         'year': '0096',
         'height': 19.7,
         'weight': 23.7,
         'pilot': '巴纳吉·林克斯',
         'description': '扎夫特军基于夺取的GAT-X系列数据开发的搭载核引擎的高性能MS，基拉·大和的座机。',
     },


     {
         'name': 'MSN-04沙扎比', 
         'series': 'UC纪元', 
         'year': '0093',
         'height': 23,
         'weight': 30.5,
         'pilot': '夏亚·阿兹纳布尔',
         'description': '扎夫特军基于夺取的GAT-X系列数据开发的搭载核引擎的高性能MS，基拉·大和的座机。',
     },

     {
         'name': 'ZGMF-X10A自由高达', 
         'series': 'SEED系列', 
         'year': 'C.E.71',
         'height': 18.03,
         'weight': 71.5,
         'pilot': '基拉·大和',
         'description': '扎夫特军基于夺取的GAT-X系列数据开发的搭载核引擎的高性能MS，基拉·大和的座机。',
     },

      {
         'name': 'ZGMF-X20A强袭自由高达', 
         'series': 'SEED系列', 
         'year': 'C.E.71',
         'pilot': '基拉·大和',
         'description': '扎夫特军基于夺取的GAT-X系列数据开发的搭载核引擎的高性能MS，基拉·大和的座机。',
     },

     {
         'name': 'MBF-P02异端高达红色机', 
         'series': 'SEED系列', 
         'year': 'C.E.71',
         'height': 17.53,
         'weight': 49.8,
         'pilot': '罗·裘尔',
         'description': '扎夫特军基于夺取的GAT-X系列数据开发的搭载核引擎的高性能MS，基拉·大和的座机。',
     },

     {
         'name': 'GAT-X105强袭高达', 
         'series': 'SEED系列', 
         'year': 'C.E.71',
         'height': 17.72,
         'weight': 64.8,
         'pilot': '基拉·大和',
         'description': '扎夫特军基于夺取的GAT-X系列数据开发的搭载核引擎的高性能MS，基拉·大和的座机。',
     },

     {
         'name': 'GN-001能天使高达', 
         'series': '00系列', 
         'year': 'A.D.2302',
         'height': 18.3,
         'weight': 57.2,
         'pilot':'刹那·F·清英',
         'description': '扎夫特军基于夺取的GAT-X系列数据开发的搭载核引擎的高性能MS，基拉·大和的座机。',
     },

     {
         'name': 'GN-000000高达', 
         'series': '00系列', 
         'year': 'A.D.2312',
         'height': 18.3,
         'weight': 54.9,
         'pilot':'刹那·F·清英',
         'description': '扎夫特军基于夺取的GAT-X系列数据开发的搭载核引擎的高性能MS，基拉·大和的座机。',
     },

      {
         'name': 'GN-002力天使高达', 
         'series': '00系列', 
         'year': 'A.D.2302',
         'height': 18.2,
         'weight': 59.1,
         'pilot':'尼尔·狄兰迪',
         'description': '扎夫特军基于夺取的GAT-X系列数据开发的搭载核引擎的高性能MS，基拉·大和的座机。',
     },

     {
         'name': 'XXXG-00W0飞翼零式高达', 
         'series': 'W系列', 
         'year': 'A.C.195',
         'height': 16.7,
         'weight': 8,
         'pilot':'希罗·尤尔',
         'description': '扎夫特军基于夺取的GAT-X系列数据开发的搭载核引擎的高性能MS，基拉·大和的座机。',
     },

     {
         'name': 'XXXG-01W飞翼高达', 
         'series': 'W系列', 
         'year': 'A.C.195',
         'height': 16.3,
         'weight': 7.1,
         'pilot':'希罗·尤尔',
         'description': '扎夫特军基于夺取的GAT-X系列数据开发的搭载核引擎的高性能MS，基拉·大和的座机。',
     },

     {
         'name': 'ASW-G-08高达巴巴托斯', 
         'series': '铁血系列', 
         'year': 'P.D——不详',
         'height': 18,
         'weight': 28.5,
         'pilot':'三日月·奥古斯',
         'description': '扎夫特军基于夺取的GAT-X系列数据开发的搭载核引擎的高性能MS，基拉·大和的座机。',
     },

     # 新增UC纪元机体
     {
         'name': 'RX-93ν高达',
         'series': 'UC纪元',
         'year': '0093',
         'height': 22,
         'weight': 27.9,
         'pilot': '阿姆罗·雷',
         'description': 'ν高达是阿姆罗·雷的最后座机，搭载了精神感应框架技术。',
     },
     
     {
         'name': 'MSN-06S新安洲',
         'series': 'UC纪元', 
         'year': '0096',
         'height': 22.6,
         'weight': 25.2,
         'pilot': '弗尔·伏朗托',
         'description': '新吉翁军的最新型MS,拥有强大的火力。',
     },
     
     {
         'name': 'MSN-04-2夜莺',
         'series': 'UC纪元',
         'year': '0093',
         'height': 22.5,
         'weight': 48.2,
         'pilot': '夏亚·阿兹纳布尔',
         'description': '夜莺是沙扎比的后继机，拥有更强的火力。',
     },
     
     {
         'name': 'RX-0独角兽高达2号机·报丧女妖',
         'series': 'UC纪元',
         'year': '0096',
         'height': 19.7,
         'weight': 23.7,
         'pilot': '马里达·克鲁斯',
         'description': '独角兽高达的2号机，被称为报丧女妖。',
     },
     
     {
         'name': 'RX-0独角兽高达3号机·菲尼克斯',
         'series': 'UC纪元',
         'year': '0095',
         'height': 19.7,
         'weight': 23.8,
         'pilot': '约拿·巴什塔',
         'description': '独角兽高达的3号机，被称为凤凰。',
     },
     #新增SEED系列机体
     {
         'name': 'MBF-02强袭嫣红',
         'series': 'SEED系列',
         'year': 'C.E.71',
         'height': 17.72,
         'weight': 64.8,
         'pilot': '卡嘉莉·尤拉·阿斯哈',
     },

     {
         'name': 'ORB-01拂晓高达',
         'series': 'SEED系列',
         'year': 'C.E.73',
         'height':18.74,
         'weight':69.6,
         'pilot': '卡嘉莉·尤拉·阿斯哈',
     },

     {
         'name': 'ZGMF-X19A无限正义高达',
         'series': 'SEED系列',
         'year': 'C.E.74',
         'height': 18.90,
         'pilot': '阿斯兰·萨拉',
     },

     {
         'name': 'ZGMF/A-262B强袭自由高达二式',
         'series': 'SEED系列',
         'year': 'C.E.75',
         'height':18.88,
         'pilot': '基拉·大和',
     },

     {
         'name': 'ZGMF/A-262PD-P非凡强袭自由高达',
         'series': 'SEED系列',
         'year': 'C.E.75',
         'height': 18.88,
         'pilot': '基拉·大和',
     },
     #新增00系列机体
     {
         'name': 'GN-003主天使高达',
         'series': '00系列',
         'year': 'A.D.2302',
         'height': 18.9,
         'weight': 54.8,
         'pilot':'阿雷路亚·哈普提森',
     },

     {
         'name': 'GN-005德天使高达',
         'series': '00系列',
         'year': 'A.D.2302',
         'height': 18.4,
         'weight': 66.7,
         'pilot':'提耶利亚·厄德',
     },

     {
         'name': 'GN-006智天使高达',
         'series': '00系列',
         'year': 'A.D.2312',
         'height': 18.0,
         'weight': 58.9,
         'pilot':'莱尔·狄兰迪',
     },
     #新增W系列机体
     {
         'name': 'XXXG-00W0飞翼零式高达EW',
         'series': 'W系列',
         'year': 'A.C.195',
         'height': 16.7,
         'weight': 8,
         'pilot':'希罗·尤尔',
     },
     #新增铁血系列机体
     {
         'name': 'ASW-G-08高达巴巴托斯·天狼座',
         'series': '铁血系列',
         'year': 'P.D.323',
         'height': 19,
         'weight': 31.2,
         'pilot':'三日月·奥古斯',
     },

     {
         'name': 'ASW-G-08高达巴巴托斯·天狼座帝王形态',
         'series': '铁血系列',
         'year': 'P.D.325',
         'height': 19,
         'weight': 31.2,
         'pilot':'三日月·奥古斯',
     },
]
# ==============================================================================

with app.app_context():
    # 确保所有表已创建
    db.create_all()

    existing_gundams = {g.name: g for g in Gundam.query.all()}
    gundams_to_add = []
    gundams_updated = 0
    gundams_skipped = 0

    print("开始检查并初始化/更新数据库中的高达基本数据...")

    for gundam_data in ALL_GUNDAM_DATA:
        if not gundam_data.get('name') or not gundam_data.get('series'):
            print(f"错误：数据条目缺少 'name' 或 'series'，已跳过: {gundam_data}")
            continue

        if gundam_data['name'] not in existing_gundams:
            # 新机体，添加到数据库
            new_gundam = Gundam(
                name=gundam_data['name'],
                series=gundam_data['series'],
                year=gundam_data.get('year'),
                height=gundam_data.get('height'),
                weight=gundam_data.get('weight'),
                pilot=gundam_data.get('pilot'),
                description=gundam_data.get('description', ''),
                image_url=gundam_data.get('image_url')
            )
            gundams_to_add.append(new_gundam)
            print(f"准备添加新机体到数据库: {gundam_data['name']} (系列: {gundam_data['series']})")
        else:
            # 现有机体，检查并更新基本信息
            existing_gundam = existing_gundams[gundam_data['name']]
            updated = False
            
            # 更新基本字段（如果提供了新值）
            if gundam_data.get('series') and existing_gundam.series != gundam_data['series']:
                existing_gundam.series = gundam_data['series']
                updated = True
            
            if gundam_data.get('year') and existing_gundam.year != gundam_data['year']:
                existing_gundam.year = gundam_data['year']
                updated = True
                
            if gundam_data.get('height') and existing_gundam.height != gundam_data['height']:
                existing_gundam.height = gundam_data['height']
                updated = True
                
            if gundam_data.get('weight') and existing_gundam.weight != gundam_data['weight']:
                existing_gundam.weight = gundam_data['weight']
                updated = True
                
            if gundam_data.get('pilot') and existing_gundam.pilot != gundam_data['pilot']:
                existing_gundam.pilot = gundam_data['pilot']
                updated = True
                
            # 描述更新（只有当现有描述为空或与提供的不同时）
            if gundam_data.get('description') and (not existing_gundam.description or existing_gundam.description != gundam_data['description']):
                existing_gundam.description = gundam_data['description']
                updated = True
                
            if gundam_data.get('image_url') and existing_gundam.image_url != gundam_data['image_url']:
                existing_gundam.image_url = gundam_data['image_url']
                updated = True
            
            if updated:
                gundams_updated += 1
                print(f"更新现有机体: {gundam_data['name']}")
            else:
                gundams_skipped += 1

    # 保存所有更改
    if gundams_to_add:
        db.session.add_all(gundams_to_add)
    
    if gundams_to_add or gundams_updated > 0:
        db.session.commit()
        print(f"成功添加 {len(gundams_to_add)} 个新机体，更新 {gundams_updated} 个现有机体。")
    else:
        print("没有新的机体需要添加或更新。")
    
    if gundams_skipped > 0:
        print(f"{gundams_skipped} 个机体无需更新。")

    print("数据库初始化/更新检查完成。") 