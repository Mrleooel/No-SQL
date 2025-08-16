from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash
from App.models.sql_models import User
from App.extensions import db
from flask_login import login_user
from werkzeug.security import check_password_hash

bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("Received form data:", request.form)
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        print(f"Found user: {user}")
        # 验证用户存在且密码正确
        if user and user.password == password:
            login_user(user)  # 关键：建立用户会话
            flash('Login successful!', 'success')
            next_page = request.args.get('next') or url_for('forum.index')  # 修复重定向目标
            return redirect(next_page)
        else:
            flash('Invalid username or password', 'danger')
        # GET 请求 → 渲染登录模板
    return render_template('auth/login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User(
            username=username,
            password=password,
            role=request.form.get('role', 'user')
        )
        db.session.add(user)
        db.session.commit()

        flash('Registration successful!')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')