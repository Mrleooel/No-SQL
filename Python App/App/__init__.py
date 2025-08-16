from flask import Flask
from flask import redirect, url_for
from .config import Config
from .extensions import login_manager, db  # 显式导入所需扩展
def create_app():
    app = Flask(__name__)
    login_manager.init_app(app)
    login_manager.login_view = 'auth/login.html'
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = '123456'
    # ---------- 初始化扩展 ----------
    from .extensions import init_extensions
    init_extensions(app)
    # ---------- 注册user_loader（关键修复点）----------
    @login_manager.user_loader
    def load_user(user_id):
        from .models.sql_models import User  # 延迟导入避免循环依赖
        return User.query.get(int(user_id))
    # ---------- 注册蓝图 ----------
    from .routes.auth import bp as auth_bp
    from .routes.forum import bp as forum_bp
    from .routes.analysis import bp as analysis_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(forum_bp, url_prefix='/forum')
    app.register_blueprint(analysis_bp, url_prefix='/analysis')
    # ---------- 初始化数据库表 ----------
    with app.app_context():
        db.create_all()

    # 添加默认路由
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    # 添加模板全局函数
    @app.context_processor
    def utility_processor():
        return {
            'max': max,
            'min': min,
            'abs': abs
        }

    return app