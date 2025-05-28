from app import create_app, db
from app.models import Gundam
import os

app = create_app()

def update_wiki_urls():
    with app.app_context():
        # 定义高达Wiki的图片URL，按系列组织
        image_urls = {
            # UC纪元系列
            'RX-78-2高达': 'https://patchwiki.biligame.com/images/gundam/b/b3/s054e54usz0d9mdtm0cc54oe68if63c.jpg',
            'MSZ-006Z高达': 'https://patchwiki.biligame.com/images/gundam/2/2c/fetakbfqd3yjery92wsz26bdx9g2xe3.jpg',
            'RX-0独角兽高达': 'https://patchwiki.biligame.com/images/gundam/7/7f/ipzah2aqs0ad4r1790le6u5at2wl313.jpg',
            # 可添加更多UC系列机体
            'MSN-04沙扎比': 'https://patchwiki.biligame.com/images/gundam/1/1e/5mmlcx0eaurqmdygro6l1ooad1beps4.jpg',
            
            # SEED系列
            'ZGMF-X10A自由高达': 'https://patchwiki.biligame.com/images/gundam/7/78/g6f7ush4gl7nn9mrcf6jpxmdyuo2iyx.jpg',
            'ZGMF-X20A强袭自由高达': 'https://patchwiki.biligame.com/images/gundam/8/84/d9jw2ee86e25bzm54enrayqmh0vsunu.jpg',
            'MBF-P02异端高达红色机': 'https://patchwiki.biligame.com/images/gundam/c/cd/mg5607rqup0lcm8h3o40vynhf9tmcru.jpg',
            'GAT-X105强袭高达': 'https://patchwiki.biligame.com/images/gundam/a/ae/i6zeorcfycxhsey9de6msk8frjwir1z.jpg',
            # 可添加更多SEED系列机体
            
            # 00系列
            'GN-001能天使高达': 'https://patchwiki.biligame.com/images/gundam/b/b2/omeeu07rfxa7jutjvqg3mh50ydiywen.jpg',
            'GN-000000高达': 'https://patchwiki.biligame.com/images/gundam/b/b8/t8fnknwalliranamsp6kh7nle150xu9.jpg',
            'GN-002力天使高达': 'https://patchwiki.biligame.com/images/gundam/8/89/ciki99558djuzzmqwsje5wdf3d1qpx2.jpg',
            # 可添加更多00系列机体
            
            # W系列
            'XXXG-00W0飞翼零式高达': 'https://patchwiki.biligame.com/images/gundam/b/b1/fa0kiq7pj1ify2lteg1j3wptz7i0gdg.jpg',
            'XXXG-01W飞翼高达': 'https://patchwiki.biligame.com/images/gundam/d/df/pxaru59domboljv3hz635toux05cz0n.jpg',
            # 可添加更多W系列机体
            
            # 铁血系列
            'ASW-G-08高达巴巴托斯': 'https://patchwiki.biligame.com/images/gundam/c/c2/o1gsyioepbzfrh62nnejg9mm54xzhtm.jpg',
            # 可添加更多铁血系列机体
            
            # 新增UC纪元机体
            'RX-93ν高达': 'https://patchwiki.biligame.com/images/gundam/f/fd/06dad23t6572ktsnnghgwiqd25ao6qu.jpg',
            'MSN-06S新安洲': 'https://patchwiki.biligame.com/images/gundam/5/5c/95fpwlghdizzs2iw53guviqllstrwrt.jpg',
            'MSN-04-2夜莺': 'https://patchwiki.biligame.com/images/gundam/3/36/cm4e223slivorj9cfkwxlgsdm54v3m0.jpg',
            'RX-0独角兽高达2号机·报丧女妖': 'https://patchwiki.biligame.com/images/gundam/6/6f/cyaq6o8c3gyscdhq2fuknkb5fwdyyb4.jpg',
            'RX-0独角兽高达3号机·菲尼克斯': 'https://patchwiki.biligame.com/images/gundam/4/41/a1sdfml8gb12gop9abadmx3qp3uwjnd.jpg',
            
            # 新增SEED系列机体
            'MBF-02强袭嫣红': 'https://patchwiki.biligame.com/images/gundam/d/db/rtd28o1bf1xw7of1o2538uaaojmmcfs.jpg',
            'ORB-01拂晓高达': 'https://patchwiki.biligame.com/images/gundam/f/f6/dile3mu3l0b6qhgli7z8loog8snwozz.jpg',
            'ZGMF-X19A无限正义高达': 'https://patchwiki.biligame.com/images/gundam/2/29/4xu91bk9r2nhpyy3n8zc3t8iv5koa13.jpg',
            'ZGMF/A-262B强袭自由高达二式': 'https://patchwiki.biligame.com/images/gundam/1/1a/irbce6ckcuy82zquojfvltkrhslzz9i.jpg',
            'ZGMF/A-262PD-P非凡强袭自由高达': 'https://patchwiki.biligame.com/images/gundam/b/bc/r6pefnvcvofk7ttyj0o6e0ikg4ow8pn.jpg',

            # 新增00系列机体
            'GN-003主天使高达': 'https://patchwiki.biligame.com/images/gundam/8/89/qezvzl0af3vbnc56s22hu3ihx299xfb.jpg',
            'GN-005德天使高达': 'https://patchwiki.biligame.com/images/gundam/6/69/4w4mcnm9jon1y8rl1e2jdj5xx2s63o8.jpg',
            'GN-006智天使高达': 'https://patchwiki.biligame.com/images/gundam/3/3f/q5hhz51l8s5cqfsk4irovqmx013eh1x.jpg', 
            # 新增W系列机体
            'XXXG-00W0飞翼零式高达EW': 'https://patchwiki.biligame.com/images/gundam/b/bb/h2g4xtosaing2jizl41rn4dax5lluun.jpg',
            # 新增铁血系列机体
            'ASW-G-08高达巴巴托斯·天狼座': 'https://patchwiki.biligame.com/images/gundam/6/6d/nn9ivhc7gve32bejda4cpi6l2gacsao.jpg',
            'ASW-G-08高达巴巴托斯·天狼座帝王形态': 'https://patchwiki.biligame.com/images/gundam/4/4a/j9wvw7pwmv3i9lk90iau9yjvag1nnjs.jpg',
        }
        
        # 查询所有高达记录并更新URL
        for gundam in Gundam.query.all():
            if gundam.name in image_urls:
                # 更新为wiki上的URL
                old_url = gundam.image_url
                gundam.image_url = image_urls[gundam.name]
                print(f"更新机体 {gundam.name}: {old_url} -> {gundam.image_url}")
            else:
                print(f"未找到匹配的URL: {gundam.name}")
        
        # 保存更改
        db.session.commit()
        print("数据库URL更新完成")

if __name__ == "__main__":
    update_wiki_urls() 