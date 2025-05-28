from flask import render_template, flash, redirect, url_for, request, current_app, jsonify
from flask_login import current_user, login_required
from app import db
from app.models import Gundam, Comment
from app.main import bp
from sqlalchemy import or_
import os # Add os import for path operations
import re # Add re import for sanitization

# --- Default values for radar chart parameters ---
DEFAULT_VALUES = {
    'size': 18.0,
    'base_weight': 50.0,
    'full_weight': 50.0,
    'engine_power': 1300.0,
    'thrust': 55000.0,
    'acceleration': 1.0
}

# --- 辅助函数，用于在后端解析参数值 ---
def parse_str_to_float(s_val):
    if not s_val or not isinstance(s_val, str):
        return None
    match = re.search(r'[+-]?([0-9]*[.])?[0-9]+', s_val)
    return float(match.group(0)) if match else None

def parse_size_py(s_val):
    if not s_val or not isinstance(s_val, str): return None
    match = re.search(r'全高：(([0-9]*[.])?[0-9]+)米?', s_val)
    if match and match.group(1): return float(match.group(1))
    match = re.search(r'头顶高：(([0-9]*[.])?[0-9]+)米?', s_val)
    if match and match.group(1): return float(match.group(1))
    match = re.search(r'(([0-9]*[.])?[0-9]+)m', s_val)
    if match and match.group(1): return float(match.group(1))
    return parse_str_to_float(s_val)

def parse_weight_py(s_val): # For t or 吨
    if not s_val or not isinstance(s_val, str): return None
    match = re.search(r'([0-9]*[.])?[0-9]+(?=(t|吨))', s_val, re.IGNORECASE)
    return float(match.group(0)) if match else parse_str_to_float(s_val)

def parse_engine_power_py(s_val): # For KW
    if not s_val or not isinstance(s_val, str): return None
    match = re.search(r'([0-9]*[.])?[0-9]+(?=KW)', s_val, re.IGNORECASE)
    return float(match.group(0)) if match else parse_str_to_float(s_val)

def parse_thrust_py(s_val): # For KG, handles "Akg x B + Ckg x D"
    if not s_val or not isinstance(s_val, str): return None
    total_thrust = 0
    complex_format_matched = False
    parts = s_val.split('+')
    if parts:
        for part in parts:
            part = part.strip()
            match = re.fullmatch(r'([0-9]*\.?[0-9]+)\s*(?:KG|kg)?\s*(?:[×x*]\s*([0-9]+))?', part, re.IGNORECASE)
            if match:
                value = float(match.group(1))
                multiplier = int(match.group(2)) if match.group(2) else 1
                total_thrust += value * multiplier
                complex_format_matched = True
            elif len(parts) == 1: 
                 complex_format_matched = False
                 break
    if complex_format_matched and total_thrust > 0:
        return total_thrust
    direct_match = re.search(r'([0-9]*[.])?[0-9]+(?=(KG|kg))', s_val, re.IGNORECASE)
    if direct_match: return float(direct_match.group(0))
    return parse_str_to_float(s_val)

def parse_acceleration_py(s_val): # For G
    if not s_val or not isinstance(s_val, str): return None
    match = re.search(r'([0-9]*[.])?[0-9]+(?=G)', s_val, re.IGNORECASE)
    return float(match.group(0)) if match else parse_str_to_float(s_val)
# --- 结束辅助函数 ---

# 新增辅助函数，用于检查图片URL是否为完整URL
def is_absolute_url(url):
    """检查URL是否为绝对URL"""
    if not url:
        return False
    return url.startswith('http://') or url.startswith('https://')

# 新增辅助函数，检查文件是否存在
def file_exists_in_static(relative_path):
    if not relative_path:
        return False
    
    # 确保路径分隔符正确
    relative_path = relative_path.replace('/', os.path.sep)
    
    # 构建完整路径
    full_path = os.path.normpath(os.path.join(current_app.static_folder, relative_path))
    
    # 检查文件是否存在
    exists = os.path.exists(full_path)
    if exists:
        print(f"文件存在: {relative_path} -> {full_path}")
    else:
        print(f"文件不存在: {relative_path} -> {full_path}")
    
    return exists

# 新增辅助函数，获取备用的占位图片路径
def get_placeholder_path():
    placeholder_img = 'images/placeholder_image.png'
    placeholder_txt = 'images/placeholder.txt'
    
    # 优先使用placeholder_image.png，如果存在
    if file_exists_in_static(placeholder_img):
        return placeholder_img
    elif file_exists_in_static(placeholder_txt):
        return placeholder_txt
    else:
        return None

# 修改该函数，确保与download_resources.py中的sanitize_filename函数完全一致
def sanitize_gundam_name_for_filename(name):
    """清理文件名中的非法字符"""
    name = re.sub(r'[\\/*?:",<>|]', '_', name)
    name = name.replace(' ', '_')
    return name

# 修改函数，添加更多的变体搜索
def find_matching_image(gundam_name):
    """根据名称尝试多种可能的文件名变体来查找图片"""
    print(f"搜索机体图片: {gundam_name}")
    
    # 1. 检查静态目录是否存在
    static_images_dir = os.path.join(current_app.static_folder, 'images')
    if not os.path.exists(static_images_dir):
        print(f"静态图片目录不存在: {static_images_dir}")
        return None
    
    # 2. 列出静态目录中的所有文件
    try:
        files = os.listdir(static_images_dir)
        print(f"图片目录中的文件: {files}")
    except Exception as e:
        print(f"列出目录失败: {e}")
        return None
    
    # 3. 尝试不同的匹配策略
    
    # 3.1 完全匹配
    for file in files:
        if file.endswith('.jpg') and gundam_name in file:
            print(f"[策略1] 完全匹配成功: {file}")
            return f'images/{file}'
    
    # 3.2 使用型号匹配
    model_name = gundam_name.split()[0] if ' ' in gundam_name else ''
    if model_name:
        for file in files:
            if file.endswith('.jpg') and model_name in file:
                print(f"[策略2] 型号匹配成功: {file}")
                return f'images/{file}'
    
    # 3.3 去除空格后匹配
    no_space_name = gundam_name.replace(' ', '')
    for file in files:
        if file.endswith('.jpg') and no_space_name in file.replace(' ', ''):
            print(f"[策略3] 无空格匹配成功: {file}")
            return f'images/{file}'
    
    # 3.4 针对中文名称的特殊匹配
    if any(ord(c) > 127 for c in gundam_name):  # 包含中文字符
        for file in files:
            # 提取中文字符并比较
            chinese_chars_in_name = ''.join([c for c in gundam_name if ord(c) > 127])
            chinese_chars_in_file = ''.join([c for c in file if ord(c) > 127])
            
            if chinese_chars_in_name and chinese_chars_in_file and \
               (chinese_chars_in_name in chinese_chars_in_file or chinese_chars_in_file in chinese_chars_in_name):
                print(f"[策略4] 中文匹配成功: {file}")
                return f'images/{file}'
    
    # 4. 回退策略：任何可能包含关键词的图片
    keywords = [word for word in gundam_name.split() if len(word) > 1 and word.isalnum()]
    if keywords:
        for keyword in keywords:
            for file in files:
                if file.endswith('.jpg') and keyword in file:
                    print(f"[策略5] 关键词匹配成功: {file}, 关键词: {keyword}")
                    return f'images/{file}'
    
    print(f"所有匹配策略均失败: {gundam_name}")
    return None

def prepare_gundam_for_view(gundam):
    """为视图准备高达机体，添加图片URL属性"""
    # 如果image_url是完整URL，直接使用
    if is_absolute_url(gundam.image_url):
        gundam.primary_image = gundam.image_url
        gundam.is_absolute_url = True
    else:
        # 使用占位符
        placeholder = get_placeholder_path()
        if placeholder:
            gundam.primary_image = placeholder
            gundam.is_absolute_url = False
        else:
            # 没有占位符，使用空字符串
            gundam.primary_image = ''
            gundam.is_absolute_url = False
    return gundam

def prepare_gundams_for_view(gundams):
    """为视图准备多个高达机体，添加图片URL属性"""
    for gundam in gundams:
        prepare_gundam_for_view(gundam)
    return gundams

@bp.route('/index')
@login_required
def index():
    # 首页路由
    # 假设您可能想要传递一些数据到首页模板，例如推荐的高达或系列
    
    return render_template('index.html', title='首页')

@bp.route('/uc_showroom')
@login_required
def uc_showroom():
    # UC演播厅页面的路由
    return render_template('UC.html', title='UC纪元演播厅')

@bp.route('/seed_showroom')
@login_required
def seed_showroom():
    return render_template('SEED.html', title='SEED演播厅')

@bp.route('/oo_showroom')
@login_required
def oo_showroom():
    return render_template('00.html', title='00演播厅')

@bp.route('/w_showroom')
@login_required
def w_showroom():
    return render_template('W.html', title='W演播厅')

@bp.route('/ibo_showroom')
@login_required
def ibo_showroom():
    return render_template('IBO.html', title='铁血的奥尔芬斯演播厅')

@bp.route('/jingxuanxilie')
@login_required
def jingxuanxilie():
    # Route for the new showcase page
    # You might want to pass data to this page later, e.g., actual featured models and series
    return render_template('jingxuanxilie.html', title='精选与系列')

@bp.route('/series/<series_name>')
@login_required
def series(series_name):
    # 系列页路由，显示特定系列的所有高达
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('GUNDAM_IMAGES_PER_PAGE', 9)
    pagination = Gundam.query.filter_by(series=series_name).paginate(
        page=page, 
        per_page=per_page,
        error_out=False
    )
    gundams_items = pagination.items
    
    # 使用工具函数批量处理图片
    prepare_gundams_for_view(gundams_items)
            
    return render_template('series.html',
                          title=f'{series_name}系列',
                          series_name=series_name,
                          gundams=gundams_items,
                          pagination=pagination)


@bp.route('/gundam/<int:id>', methods=['GET', 'POST'])
def gundam_detail(id):
    gundam = Gundam.query.get_or_404(id)
    print(f"处理详情页机体: {gundam.name}")
    
    prepare_gundam_for_view(gundam)
    primary_image = gundam.primary_image
    is_absolute_url_flag = gundam.is_absolute_url
    additional_images = [] 

    # Helper map for parsing functions
    parsing_map = {
        'size': parse_size_py, 'base_weight': parse_weight_py, 'full_weight': parse_weight_py,
        'engine_power': parse_engine_power_py, 'thrust': parse_thrust_py, 'acceleration': parse_acceleration_py
    }

    # Calculate max_radar_params using defaults where necessary
    all_gundams_data = Gundam.query.all()
    max_params = {key: 0.0 for key in DEFAULT_VALUES} # Initialize with 0 or very small numbers

    for item in all_gundams_data:
        item_raw_values = {
            'size': item.size, 'base_weight': item.base_weight, 'full_weight': item.full_weight,
            'engine_power': item.engine_power, 'thrust': item.thrust, 'acceleration': item.acceleration
        }
        for key, raw_val in item_raw_values.items():
            val_for_max_calc = None
            if raw_val == '-' or raw_val == '0':
                val_for_max_calc = DEFAULT_VALUES[key]
            else:
                parsed_val = parsing_map[key](raw_val)
                if parsed_val is None or parsed_val == 0:
                    val_for_max_calc = DEFAULT_VALUES[key]
                else:
                    val_for_max_calc = parsed_val
            
            if val_for_max_calc is not None and val_for_max_calc > max_params[key]:
                max_params[key] = val_for_max_calc
    
    # Ensure max_params are at least their default values or 1 if default is less (e.g. acceleration)
    # or a slightly larger sensible minimum if all actual/default values were 0 (though unlikely with defaults)
    for key in max_params:
        if max_params[key] <= 0: # If still 0 after processing all gundams
             max_params[key] = DEFAULT_VALUES[key] # Use default as max
        # Ensure a minimum axis value if max_params[key] is very small, e.g. for acceleration
        if key == 'acceleration' and max_params[key] < 1.0:
            max_params[key] = 1.0 # Smallest sensible max for G
        elif max_params[key] < 1.0 and max_params[key] > 0: # for other very small positive values
             pass # keep it if it's a real small max
        elif max_params[key] == 0 : # If somehow it's still zero (e.g. default was 0)
             max_params[key] = 1 # Fallback to 1 to prevent ECharts error with max 0


    # Prepare processed tech parameters for the current gundam for the template
    tech_data_for_template = {}
    current_gundam_raw_values = {
        'size': gundam.size, 'base_weight': gundam.base_weight, 'full_weight': gundam.full_weight,
        'engine_power': gundam.engine_power, 'thrust': gundam.thrust, 'acceleration': gundam.acceleration
    }

    for key, raw_val in current_gundam_raw_values.items():
        if raw_val == '-' or raw_val == '0':
            tech_data_for_template[key] = DEFAULT_VALUES[key]
        else:
            parsed_val = parsing_map[key](raw_val)
            if parsed_val is None or parsed_val == 0:
                tech_data_for_template[key] = DEFAULT_VALUES[key]
            else:
                tech_data_for_template[key] = parsed_val
    
    gundam_description_updated = gundam.description 

    # --- Prepare data for Series Timeline ---
    series_timeline_data = []
    if gundam.series:
        same_series_gundams = Gundam.query.filter_by(series=gundam.series).order_by(Gundam.year, Gundam.id).all()
        for s_gundam in same_series_gundams:
            series_timeline_data.append({
                'id': s_gundam.id,
                'name': s_gundam.name,
                'year': s_gundam.year if s_gundam.year else "未知", # Handle cases where year might be None
                'is_current': s_gundam.id == gundam.id
            })
    # --- End Series Timeline data --- 

    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.filter_by(gundam_id=id).order_by(
        Comment.timestamp.desc()
    ).paginate(
        page=page,
        per_page=10,
        error_out=False
    )
    comments = pagination.items
    
    return render_template('detail.html',
                          title=gundam.name,
                          gundam=gundam,
                          primary_image=primary_image,
                          is_absolute_url=is_absolute_url_flag,
                          additional_images=additional_images,
                          comments=comments,
                          pagination=pagination,
                          gundam_description_updated=gundam_description_updated,
                          tech_params_radar=tech_data_for_template,
                          max_radar_params=max_params,
                          series_timeline_data=series_timeline_data # Pass timeline data to template
                          )

@bp.route('/gundam/<int:id>/comment', methods=['POST'])
@login_required
def add_comment(id):
    # 添加评论路由
    gundam = Gundam.query.get_or_404(id)
    content = request.form.get('content')
    
    if not content:
        flash('评论不能为空！', 'danger')
    else:
        comment = Comment(content=content, author=current_user, gundam=gundam)
        db.session.add(comment)
        db.session.commit()
        flash('评论发表成功！', 'success')
    
    return redirect(url_for('main.gundam_detail', id=id))


@bp.route('/search')
def search():
    # 搜索路由，支持机体名称、系列、驾驶员的搜索
    query = request.args.get('q', '')
    if not query:
        return redirect(url_for('main.index'))
    
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('GUNDAM_IMAGES_PER_PAGE', 9)
    
    # 使用or_进行多字段模糊搜索
    search_pagination = Gundam.query.filter(
        or_(
            Gundam.name.like(f'%{query}%'),
            Gundam.series.like(f'%{query}%'),
            Gundam.pilot.like(f'%{query}%'),
            Gundam.description.like(f'%{query}%')
        )
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    search_results_items = search_pagination.items
    # 使用工具函数批量处理图片
    prepare_gundams_for_view(search_results_items)

    return render_template('search.html',
                          title=f'搜索: {query}',
                          query=query,
                          results=search_results_items,
                          pagination=search_pagination)


@bp.route('/api/gundams')
def api_gundams():
    # API路由，返回所有高达数据
    series = request.args.get('series')
    limit = request.args.get('limit', default=10, type=int)
    
    query = Gundam.query
    
    if series:
        query = query.filter_by(series=series)
    
    gundams = query.limit(limit).all()
    
    result = []
    for gundam_item in gundams:
        # 使用工具函数处理图片
        prepare_gundam_for_view(gundam_item)
        image_url = gundam_item.primary_image
        
        if not is_absolute_url(image_url) and image_url:
            # 如果不是绝对URL但有图片路径，生成完整URL
            image_url = url_for('static', filename=image_url, _external=True)

        result.append({
            'id': gundam_item.id,
            'name': gundam_item.name,
            'series': gundam_item.series,
            'year': gundam_item.year,
            'pilot': gundam_item.pilot,
            'height': gundam_item.height,
            'weight': gundam_item.weight,
            'image_url': image_url
        })
    
    return jsonify(result)


@bp.route('/api/gundam/<int:id>')
def api_gundam_detail(id):
    gundam = Gundam.query.get_or_404(id)
    
    # 使用工具函数处理图片
    prepare_gundam_for_view(gundam)
    
    # 确定图片URLs
    image_urls = []
    primary_image_url = None
    
    if gundam.is_absolute_url:
        primary_image_url = gundam.primary_image
        image_urls.append(primary_image_url)
    else:
        if gundam.primary_image:
            primary_image_url = url_for('static', filename=gundam.primary_image, _external=True)
            image_urls.append(primary_image_url)
    
    # 收集评论
    comments = []
    for comment_item in gundam.comments:
        comments.append({
            'id': comment_item.id,
            'content': comment_item.content,
            'timestamp': comment_item.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'author': comment_item.author.username
        })
    
    # 确定模型URL
    model_url = None
    if gundam.model_url:
        if is_absolute_url(gundam.model_url):
            model_url = gundam.model_url
        elif file_exists_in_static(gundam.model_url):
            model_url = url_for('static', filename=gundam.model_url, _external=True)
    
    result = {
        'id': gundam.id,
        'name': gundam.name,
        'series': gundam.series,
        'year': gundam.year,
        'pilot': gundam.pilot,
        'height': gundam.height,
        'weight': gundam.weight,
        'description': gundam.description,
        'image_url': primary_image_url,
        'all_image_urls': image_urls,
        'model_url': model_url,
        'comments': comments
    }
    
    return jsonify(result)


@bp.route('/api/search')
def api_search():
    # API搜索路由
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    
    limit = request.args.get('limit', default=10, type=int)
    
    search_results = Gundam.query.filter(
        or_(
            Gundam.name.like(f'%{query}%'),
            Gundam.series.like(f'%{query}%'),
            Gundam.pilot.like(f'%{query}%'),
            Gundam.description.like(f'%{query}%')
        )
    ).limit(limit).all()
    
    result = []
    for gundam in search_results:
        # 使用工具函数处理图片
        prepare_gundam_for_view(gundam)
        
        # 准备API返回的图片URL
        image_url = None
        if gundam.is_absolute_url:
            image_url = gundam.primary_image
        elif gundam.primary_image:
            image_url = url_for('static', filename=gundam.primary_image, _external=True)

        result.append({
            'id': gundam.id,
            'name': gundam.name,
            'series': gundam.series,
            'pilot': gundam.pilot,
            'image_url': image_url
        })
    
    return jsonify(result)

@bp.route('/comment/<int:id>/delete', methods=['POST'])
@login_required
def delete_comment(id):
    # 删除评论
    comment = Comment.query.get_or_404(id)
    if not current_user.is_authenticated:
        flash('您必须登录才能删除评论！', 'danger')
        return redirect(url_for('main.gundam_detail', id=comment.gundam_id))
    
    # 只有评论作者或管理员可以删除评论
    if comment.author != current_user and not current_user.is_admin:
        flash('您没有权限删除此评论！', 'danger')
        return redirect(url_for('main.gundam_detail', id=comment.gundam_id))
    
    gundam_id = comment.gundam_id
    db.session.delete(comment)
    db.session.commit()
    
    flash('评论已删除！', 'success')
    return redirect(url_for('main.gundam_detail', id=gundam_id)) 

@bp.route('/album')
@login_required
def album():
    return render_template('ALBUM.html')

@bp.route('/blog_join')
@login_required
def blog_join():
    return render_template('blog_join.html')

 