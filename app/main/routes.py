from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required
from app import db
from app.models import Gundam, Comment
from app.main import bp


@bp.route('/')
@bp.route('/index')
def index():
    # 首页路由，显示高达系列概览
    series_list = db.session.query(Gundam.series).distinct().all()
    series_list = [s[0] for s in series_list]  # 转换为列表
    
    # 获取每个系列的一个代表性机体作为展示
    featured_gundams = []
    for series in series_list:
        gundam = Gundam.query.filter_by(series=series).first()
        if gundam:
            featured_gundams.append(gundam)
    
    return render_template('index.html', 
                          title='高达信息展示平台', 
                          featured_gundams=featured_gundams,
                          series_list=series_list)


@bp.route('/series/<series_name>')
def series(series_name):
    # 系列页路由，显示特定系列的所有高达
    page = request.args.get('page', 1, type=int)
    pagination = Gundam.query.filter_by(series=series_name).paginate(
        page=page, 
        per_page=current_app.config['GUNDAM_IMAGES_PER_PAGE'],
        error_out=False
    )
    gundams = pagination.items
    
    return render_template('series.html',
                          title=f'{series_name}系列',
                          series_name=series_name,
                          gundams=gundams,
                          pagination=pagination)


@bp.route('/gundam/<int:id>', methods=['GET', 'POST'])
def gundam_detail(id):
    # 高达详情页路由，显示特定高达的详细信息和评论
    gundam = Gundam.query.get_or_404(id)
    
    # 获取评论
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
                          comments=comments,
                          pagination=pagination)


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