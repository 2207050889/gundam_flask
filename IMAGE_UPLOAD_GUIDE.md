# 高达机体图片上传指南

## 图片目录结构

```
app/static/images/
├── thumbnails/     # 缩略图 (用于系列页、搜索页)
├── details/        # 详情页高清大图
├── backgrounds/    # 详情页背景图 (你的本地大图)
├── series/         # 系列封面图
└── showcase/       # 展示图片
```

## 图片规格建议

### 1. 缩略图 (thumbnails/)
- **尺寸**: 200x200px 或 300x300px
- **格式**: JPG/PNG
- **用途**: 系列页网格显示、搜索结果
- **命名**: `{机体英文名}_thumb.jpg`
- **示例**: `nu_gundam_thumb.jpg`

### 2. 详情页大图 (details/)
- **尺寸**: 800x600px 或更高
- **格式**: JPG/PNG
- **用途**: 机体详情页主要展示图
- **命名**: `{机体英文名}_detail.jpg`
- **示例**: `nu_gundam_detail.jpg`

### 3. 背景图 (backgrounds/)
- **尺寸**: 1920x1080px 或更高
- **格式**: JPG (推荐，文件更小)
- **用途**: 详情页背景，营造氛围
- **命名**: `{机体英文名}_bg.jpg`
- **示例**: `nu_gundam_bg.jpg`

## 上传步骤

### 方法1: 直接复制文件
1. 将准备好的图片文件复制到对应目录
2. 确保文件名符合命名规范
3. 运行图片管理脚本更新数据库

### 方法2: 使用图片管理工具
```bash
# 1. 先添加图片字段到数据库
python scripts/add_image_fields.py

# 2. 运行图片管理工具
python scripts/manage_images.py
```

## 当前需要图片的机体

### UC纪元系列 (需要本地图片)
- RX-93ν高达 (`nu_gundam_*`)
- MSN-06S新安洲 (`sinanju_*`)
- RX-93-ν2Hi-ν高达 (`hi_nu_*`)
- MSN-04-2夜莺 (`nightingale_*`)
- RX-0独角兽高达2号机报丧女妖 (`banshee_*`)
- RX-0独角兽高达3号机凤凰 (`phenex_*`)

### SEED系列 (需要本地图片)
- MBF-02强袭嫣红 (`rouge_*`)

## 图片获取建议

### 1. 官方来源
- 万代官网产品图
- 动画截图
- 游戏内模型图

### 2. 高质量同人图
- Pixiv高分辨率作品
- DeviantArt作品
- 模型摄影作品

### 3. 背景图制作
- 使用PS/GIMP添加光效
- 星空/宇宙背景
- 机体剪影效果
- 渐变色背景

## 批量处理建议

### 使用PowerShell批量重命名
```powershell
# 进入图片目录
cd app/static/images/backgrounds

# 批量重命名示例
Rename-Item "ν高达背景.jpg" "nu_gundam_bg.jpg"
Rename-Item "新安洲背景.jpg" "sinanju_bg.jpg"
```

### 使用Python脚本批量处理
```python
import os
from PIL import Image

def resize_images(input_dir, output_dir, size):
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.jpg', '.png')):
            img = Image.open(os.path.join(input_dir, filename))
            img = img.resize(size, Image.Resampling.LANCZOS)
            img.save(os.path.join(output_dir, filename))
```

## 注意事项

1. **文件大小控制**
   - 缩略图: < 100KB
   - 详情图: < 500KB  
   - 背景图: < 2MB

2. **版权问题**
   - 优先使用官方图片
   - 注明图片来源
   - 避免使用有版权争议的图片

3. **命名规范**
   - 使用英文命名
   - 避免特殊字符和空格
   - 保持命名一致性

4. **备份**
   - 保留原始高分辨率图片
   - 定期备份图片文件夹

## 完整操作流程

1. **准备图片文件**
   ```
   你的图片文件夹/
   ├── ν高达_缩略图.jpg
   ├── ν高达_详情图.jpg
   ├── ν高达_背景图.jpg
   └── ...
   ```

2. **重命名并复制到项目**
   ```bash
   # 复制到对应目录
   copy "ν高达_缩略图.jpg" "app/static/images/thumbnails/nu_gundam_thumb.jpg"
   copy "ν高达_详情图.jpg" "app/static/images/details/nu_gundam_detail.jpg"  
   copy "ν高达_背景图.jpg" "app/static/images/backgrounds/nu_gundam_bg.jpg"
   ```

3. **更新数据库**
   ```bash
   # 添加图片字段
   python scripts/add_image_fields.py
   
   # 更新图片URL
   python scripts/manage_images.py
   ```

4. **验证效果**
   ```bash
   # 启动服务器查看效果
   python run.py
   ``` 