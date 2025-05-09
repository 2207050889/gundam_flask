# 高达主题互动式信息展示平台

## 项目简介
这是一个基于Flask框架开发的高达主题信息展示平台，提供机动战士高达系列相关的机体资料与互动功能。本项目是福州英华职业学院人工智能技术应用专业毕业设计作品。

## 功能特点
- **静态内容分类展示**：按UC纪元、SEED系列等分类展示高达机体信息
- **用户留言板功能**：支持用户注册、登录、评论提交与查看
- **3D模型预览**：使用Three.js实现RX-78-2等经典机体的交互式3D模型展示

## 技术栈
- **后端**：Python Flask + SQLite
- **前端**：Jinja2 + Bootstrap + JavaScript (Three.js)
- **部署**：Heroku/GitHub Pages

## 环境要求
- Python 3.8+
- 详细依赖请参考requirements.txt

## 安装与运行
1. 克隆代码库
```bash
git clone https://github.com/yourusername/gundam_flask.git
cd gundam_flask
```

2. 创建并激活虚拟环境
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 初始化数据库
```bash
flask shell
>>> from app import db
>>> db.create_all()
>>> exit()
```

5. 运行应用
```bash
flask run
```

## 项目结构
```
gundam_flask/
├── app/                  # 应用主目录
│   ├── static/           # 静态文件
│   ├── templates/        # 模板文件
│   ├── models.py         # 数据模型
│   ├── routes.py         # 路由
│   └── __init__.py       # 应用初始化
├── instance/             # 实例文件夹
├── config.py             # 配置文件
├── requirements.txt      # 依赖列表
└── run.py                # 运行入口
```

## 开发计划
- [x] 需求与设计
- [ ] 数据收集与整理
- [ ] 后端开发
- [ ] 前端开发
- [ ] 测试与部署
- [ ] 文档完善

## 作者
- 傅华盛（福州英华职业学院人工智能技术应用专业）

## 指导教师
- 张善钦

## 许可证
本项目仅用于学习和研究目的。高达相关内容版权归BANDAI NAMCO所有。 