from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import db
from app.auth import bp
from app.models import User, Comment


@bp.route('/login', methods=['GET', 'POST'])
def login():
    # 登录路由
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user is None or not user.check_password(password):
            flash('用户名或密码错误', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        
        flash('登录成功！', 'success')
        return redirect(next_page)
    
    return render_template('auth/login.html', title='登录')


@bp.route('/logout')
def logout():
    # 登出路由
    logout_user()
    flash('已成功登出', 'info')
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    # 注册路由
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        
        # 简单验证
        if not all([username, email, password, password2]):
            flash('所有字段都必须填写', 'danger')
            return redirect(url_for('auth.register'))
        
        if password != password2:
            flash('两次输入的密码不一致', 'danger')
            return redirect(url_for('auth.register'))
        
        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            flash('该用户名已被使用', 'danger')
            return redirect(url_for('auth.register'))
        
        # 检查邮箱是否已存在
        if User.query.filter_by(email=email).first():
            flash('该邮箱已被注册', 'danger')
            return redirect(url_for('auth.register'))
        
        # 创建新用户
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('注册成功，请登录！', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='注册')


@bp.route('/profile')
@login_required
def profile():
    # 用户个人资料页面
    # 获取用户的评论
    comments = Comment.query.filter_by(user_id=current_user.id)\
                       .order_by(Comment.timestamp.desc()).all()
    
    return render_template('auth/profile.html', 
                          title='个人资料',
                          user=current_user,
                          comments=comments)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    # 编辑个人资料
    if request.method == 'POST':
        email = request.form.get('email')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        password2 = request.form.get('password2')
        
        # 验证
        if email != current_user.email:
            # 检查邮箱是否已被其他用户使用
            if User.query.filter(User.email == email, User.id != current_user.id).first():
                flash('该邮箱已被注册', 'danger')
                return redirect(url_for('auth.edit_profile'))
            
            # 更新邮箱
            current_user.email = email
        
        # 如果提供了当前密码和新密码，则更改密码
        if current_password and new_password and password2:
            if not current_user.check_password(current_password):
                flash('当前密码不正确', 'danger')
                return redirect(url_for('auth.edit_profile'))
                
            if new_password != password2:
                flash('两次输入的新密码不一致', 'danger')
                return redirect(url_for('auth.edit_profile'))
                
            current_user.set_password(new_password)
            flash('密码已成功更新', 'success')
        
        # 保存更改
        db.session.commit()
        flash('个人资料已更新', 'success')
        return redirect(url_for('auth.profile'))
        
    return render_template('auth/edit_profile.html', title='编辑个人资料') 