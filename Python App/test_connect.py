from pymongo import MongoClient
import pyodbc
import sys
from App.config import Config

config = Config()


def test_mongodb_connection():
    """测试MongoDB服务器连接（不依赖特定数据库）"""
    try:
        client = MongoClient(config.MONGO_URI)
        result = client.admin.command('ping')
        print(f"✅ MongoDB服务器连接成功! Ping响应: {result['ok']}")

        # 尝试连接默认数据库
        try:
            db = client.get_database(config.MONGO_DB_NAME)
            print(f"   默认数据库状态: {config.MONGO_DB_NAME} (存在: {db.name})")
        except Exception as e:
            print(f"   默认数据库创建状态: {config.MONGO_DB_NAME} (未创建, 可使用db.create_database()创建)")
        return True
    except Exception as e:
        print(f"❌ MongoDB连接失败: {e}")
        return False


def test_sqlserver_connection():
    """测试SQL Server连接（使用默认master数据库）"""
    try:
        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={config.SQL_SERVER};"
            f"DATABASE={config.SQL_DB};"
            "Trusted_Connection=yes;"
        )
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        # 验证Windows身份 - 修复语法错误 ✅
        # 使用方括号解决关键字冲突问题
        cursor.execute("SELECT @@VERSION AS version, CURRENT_USER AS [current_user]")
        result = cursor.fetchone()
        # 检查目标数据库是否存在
        cursor.execute(
            "SELECT name FROM sys.databases WHERE name = ?",
            config.SQL_DB
        )
        db_exists = cursor.fetchone()
        print(f"✅ SQL Server连接成功!")
        print(f"   当前用户: {result.current_user}")  # 注意这里改为获取current_user属性
        print(f"   目标数据库: {config.SQL_DB} (存在: {bool(db_exists)})")
        return True
    except pyodbc.Error as e:
        # 增强错误信息处理
        error_msg = "❌ SQL Server连接失败: " + str(e).replace('\n', ' ')
        print(error_msg)

        # 提供具体解决方案提示
        if '156' in str(e):  # 关键字错误
            print("   ➡️ 解决方案: 避免在没有方括号的情况下使用SQL关键字作为列别名")
        elif 'HYT00' in str(e):  # 连接超时
            print("   ➡️ 解决方案: 检查SQL Server是否运行中，确认服务器地址和防火墙设置")
        return False


if __name__ == '__main__':
    print("\n=== 数据库连接测试开始 ===")

    print("\n[1] MongoDB连接测试:")
    mongo_success = test_mongodb_connection()

    print("\n[2] SQL Server连接测试:")
    sql_success = test_sqlserver_connection()

    print("\n=== 测试总结 ===")
    print(f"MongoDB: {'成功' if mongo_success else '失败'}")
    print(f"SQL Server: {'成功' if sql_success else '失败'}")

    # 返回测试结果码
    sys.exit(0 if all([mongo_success, sql_success]) else 1)



    # index.html
# {% extends "base.html" %}
# {% macro render_pagination(pagination) %}
# <!-- app/templates/macros/pagination.html -->
# {% macro render_pagination(pagination, endpoint) %}
#   <nav aria-label="Page navigation">
#     <ul class="pagination justify-content-center">
#       {% if pagination.has_prev %}
#         <li class="page-item">
#           <a class="page-link" href="{{ url_for(endpoint, page=pagination.prev_num, **kwargs) }}">
#             &laquo;
#           </a>
#         </li>
#       {% else %}
#         <li class="page-item disabled">
#           <span class="page-link">&laquo;</span>
#         </li>
#       {% endif %}
#       {%- for page in pagination.iter_pages() %}
#         {% if page %}
#           {% if page != pagination.page %}
#             <li class="page-item">
#               <a class="page-link" href="{{ url_for(endpoint, page=page, **kwargs) }}">{{ page }}</a>
#             </li>
#           {% else %}
#             <li class="page-item active">
#               <span class="page-link">{{ page }}</span>
#             </li>
#           {% endif %}
#         {% else %}
#           <li class="page-item disabled">
#             <span class="page-link">...</span>
#           </li>
#         {% endif %}
#       {%- endfor %}
#       {% if pagination.has_next %}
#         <li class="page-item">
#           <a class="page-link" href="{{ url_for(endpoint, page=pagination.next_num, **kwargs) }}">
#             &raquo;
#           </a>
#         </li>
#       {% else %}
#         <li class="page-item disabled">
#           <span class="page-link">&raquo;</span>
#         </li>
#       {% endif %}
#     </ul>
#   </nav>
# {% endmacro %}
# {% endmacro %}
# {% block head %}
#     {{ super() }}
#     <!-- 引入Tailwind CSS -->
#     <script src="https://cdn.tailwindcss.com"></script>
#     <!-- 引入Font Awesome -->
#     <link href="https://cdn.jsdelivr.net/npm/font-awesome@4.7.0/css/font-awesome.min.css" rel="stylesheet">
#
#     <!-- 自定义Tailwind配置 -->
#     <script>
#         tailwind.config = {
#             theme: {
#                 extend: {
#                     colors: {
#                         primary: '#165DFF',
#                         secondary: '#36D399',
#                         neutral: {
#                             100: '#F9FAFB',
#                             200: '#F3F4F6',
#                             300: '#E5E7EB',
#                             400: '#D1D5DB',
#                             500: '#9CA3AF',
#                             600: '#6B7280',
#                             700: '#4B5563',
#                             800: '#1F2937',
#                             900: '#111827',
#                         },
#                     },
#                     fontFamily: {
#                         inter: ['Inter', 'system-ui', 'sans-serif'],
#                     },
#                     boxShadow: {
#                         'card': '0 10px 25px -5px rgba(0, 0, 0, 0.05)',
#                         'card-hover': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
#                         'nav': '0 2px 10px rgba(0, 0, 0, 0.05)',
#                     },
#                     animation: {
#                         'bounce-subtle': 'bounceSubtle 2s infinite',
#                     },
#                     keyframes: {
#                         bounceSubtle: {
#                             '0%, 100%': { transform: 'translateY(0)' },
#                             '50%': { transform: 'translateY(-2px)' },
#                         }
#                     }
#                 },
#             }
#         }
#     </script>
#
#     <!-- 自定义工具类 -->
#     <style type="text/tailwindcss">
#         @layer utilities {
#             .content-auto {
#                 content-visibility: auto;
#             }
#             .author-info {
#                 @apply flex items-center text-sm text-neutral-600;
#             }
#             .post-meta {
#                 @apply flex flex-wrap gap-3 mt-2 text-sm text-neutral-500;
#             }
#             .action-buttons {
#                 @apply flex gap-2 mt-4;
#             }
#             .hover-scale {
#                 @apply transition-transform duration-300 hover:scale-105;
#             }
#         }
#     </style>
#
#     <style>
#         @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
#
#         ::-webkit-scrollbar {
#             width: 8px;
#             height: 8px;
#         }
#         ::-webkit-scrollbar-track {
#             background: #f1f1f1;
#             border-radius: 4px;
#         }
#         ::-webkit-scrollbar-thumb {
#             background: #d1d5db;
#             border-radius: 4px;
#         }
#         ::-webkit-scrollbar-thumb:hover {
#             background: #9ca3af;
#         }
#
#         .fade-in {
#             animation: fadeIn 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards;
#         }
#         @keyframes fadeIn {
#             from { opacity: 0; transform: translateY(15px); }
#             to { opacity: 1; transform: translateY(0); }
#         }
#
#         .nav-scrolled {
#             background-color: rgba(255, 255, 255, 0.95);
#             backdrop-filter: blur(8px);
#             transition: background-color 0.3s, box-shadow 0.3s;
#         }
#     </style>
# {% endblock %}
#
# {% block content %}
# {{ render_pagination(pagination) }}
# <div class="container mx-auto px-4 py-8 max-w-7xl">
#     <!-- 标题和新建按钮 -->
#     <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 fade-in">
#         <div>
#             <h1 class="text-[clamp(1.8rem,3vw,2.5rem)] font-bold text-neutral-800 mb-2 flex items-center">
#                 <i class="fa fa-comments text-primary mr-3 text-[clamp(1.8rem,3vw,2.5rem)] animate-bounce-subtle"></i>
#                 Community Forum
#             </h1>
#             <p class="text-neutral-600 text-lg max-w-2xl text-balance">Join the discussion and share your thoughts with our vibrant community</p>
#         </div>
#         <a href="{{ url_for('forum.create_post') }}"
#            class="mt-4 md:mt-0 bg-primary hover:bg-primary/90 text-white font-medium px-6 py-3 rounded-lg shadow-lg hover:shadow-xl btn-pulse flex items-center">
#             <i class="fa fa-plus mr-2"></i> New Post
#         </a>
#     </div>
#
#     <!-- 搜索面板 -->
#     <div class="bg-white rounded-2xl shadow-card p-6 md:p-8 mb-8 transition-all duration-300 hover-lift fade-in">
#         <form method="get" action="{{ url_for('forum.index') }}" class="space-y-6">
#             <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
#                 <!-- 关键词搜索 -->
#                 <div>
#                     <label for="keyword" class="block text-sm font-medium text-neutral-700 mb-2">Search</label>
#                     <div class="relative">
#                         <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-neutral-500">
#                             <i class="fa fa-search"></i>
#                         </span>
#                         <input type="text" id="keyword" name="keyword" class="w-full pl-10 pr-4 py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary/50 focus:border-primary outline-none transition-all"
#                                placeholder="Search posts by title or content..." value="{{ search_params.keyword }}">
#                     </div>
#                 </div>
#
#                 <!-- 作者筛选 -->
#                 <div>
#                     <label for="author_id" class="block text-sm font-medium text-neutral-700 mb-2">Author</label>
#                     <div class="relative">
#                         <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-neutral-500">
#                             <i class="fa fa-user"></i>
#                         </span>
#                         <input type="text" id="author_id" name="author_id" class="w-full pl-10 pr-4 py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary/50 focus:border-primary outline-none transition-all"
#                                placeholder="Enter author ID or username" value="{{ search_params.author_id }}">
#                     </div>
#                 </div>
#
#                 <!-- 日期范围 -->
#                 <div>
#                     <div class="flex justify-between items-center mb-2">
#                         <label for="start_date" class="block text-sm font-medium text-neutral-700">Start Date</label>
#                         <label for="end_date" class="block text-sm font-medium text-neutral-700">End Date</label>
#                     </div>
#                     <div class="grid grid-cols-2 gap-3">
#                         <div class="relative">
#                             <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-neutral-500">
#                                 <i class="fa fa-calendar"></i>
#                             </span>
#                             <input type="date" id="start_date" name="start_date" class="w-full pl-10 pr-4 py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary/50 focus:border-primary outline-none transition-all"
#                                    value="{{ search_params.start_date }}" placeholder="Start date">
#                         </div>
#                         <div class="relative">
#                             <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-neutral-500">
#                                 <i class="fa fa-calendar"></i>
#                             </span>
#                             <input type="date" id="end_date" name="end_date" class="w-full pl-10 pr-4 py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary/50 focus:border-primary outline-none transition-all"
#                                    value="{{ search_params.end_date }}" placeholder="End date">
#                         </div>
#                     </div>
#                 </div>
#
#                 <!-- 操作按钮 -->
#                 <div class="flex items-end">
#                     <button type="submit" class="w-full bg-primary hover:bg-primary/90 text-white font-medium px-6 py-3 rounded-lg shadow transition-all duration-300 flex items-center justify-center btn-pulse">
#                         <i class="fa fa-filter mr-2"></i> Filter Results
#                     </button>
#                 </div>
#             </div>
#         </form>
#     </div>
#
#     <!-- 帖子列表 -->
#     <div class="space-y-6">
#         {% for post in posts %}
#         <div class="bg-white rounded-2xl shadow-card p-6 md:p-8 hover-lift fade-in" style="animation-delay: {{ loop.index * 0.1 }}s">
#             <!-- 帖子头部：标题和用户信息 -->
#             <div class="mb-6">
#                 <h3 class="text-xl md:text-2xl font-semibold text-neutral-800 mb-2">
#                     <a href="{{ url_for('forum.view_post', post_id=post._id) }}" class="hover:text-primary transition-colors duration-300">
#                         {{ post.title }}
#                     </a>
#                     {% if post.created_at.date() == datetime.utcnow().date() %}
#                     <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800 ml-2 animate-pulse">
#                         <i class="fa fa-circle text-green-500 text-[8px] mr-1"></i>
#                     </span>
#                     {% endif %}
#                 </h3>
#
#                 <!-- 用户名在左侧，操作按钮在右侧（小屏幕下堆叠） -->
#                 <div class="flex flex-col md:flex-row md:items-center justify-between">
#                     <div class="author-info">
#                         <i class="fa fa-user-circle-o mr-1.5 text-neutral-500"></i>
#                         <a href="{{ url_for('forum.index', author_id=post.author_id) }}" class="text-primary hover:underline transition-colors">
#                             {{ post.author_id|truncate(10) }}
#                         </a>
#                         <span class="mx-2.5 text-neutral-400">•</span>
#                         <i class="fa fa-clock-o mr-1.5 text-neutral-500"></i>
#                         {{ post.created_at.strftime("%Y-%m-%d %H:%M") }}
#                         {% if post.updated_at %}
#                             <span class="mx-2.5 text-neutral-400">•</span>
#                             <span class="text-neutral-500">Updated: {{ post.updated_at.strftime("%Y-%m-%d") }}</span>
#                         {% endif %}
#                     </div>
#
#                     <!-- 删除按钮放在下方（小屏幕）或右侧（大屏幕） -->
#                     {% if post.author_id == current_user_id %}
#                     <div class="mt-3 md:mt-0">
#                         <div class="dropdown relative">
#                             <button class="btn btn-sm btn-outline-secondary dropdown-toggle"
#                                     type="button" data-bs-toggle="dropdown" aria-expanded="false">
#                                 <i class="fa fa-ellipsis-v text-neutral-500"></i>
#                             </button>
#                             <ul class="dropdown-menu absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg py-1 z-10 border-0">
#                                 <li>
#                                     <form action="{{ url_for('forum.delete_post', post_id=post._id) }}"
#                                           method="POST" class="d-inline">
#                                         <button type="submit" class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
#                                                 onclick="return confirm('Delete this post permanently? This action cannot be undone.')">
#                                             <i class="fa fa-trash mr-2 text-red-500"></i> Delete Post
#                                         </button>
#                                     </form>
#                                 </li>
#                             </ul>
#                         </div>
#                     </div>
#                     {% endif %}
#                 </div>
#             </div>
#
#             <!-- 帖子内容：显示在用户名下方/右侧 -->
#             <p class="text-neutral-700 mb-6 leading-relaxed">
#                 {{ post.content|truncate(200) }}
#             </p>
#
#             <!-- 标签展示 -->
#             {% if post.tags %}
#             <div class="flex flex-wrap gap-2 mb-6">
#                 {% for tag in post.tags %}
#                 <span class="inline-flex items-center px-3.5 py-1.5 rounded-full text-sm font-medium bg-neutral-100 text-neutral-700 hover:bg-primary hover:text-white transition-colors duration-300">
#                     <i class="fa fa-tag mr-1.5 text-neutral-500"></i>{{ tag }}
#                 </span>
#                 {% endfor %}
#             </div>
#             {% endif %}
#
#             <!-- 底部交互区：点赞、评论和阅读更多 -->
#             <div class="pt-6 border-t border-neutral-100">
#                 <div class="action-buttons">
#                     <button class="flex items-center text-neutral-500 hover:text-primary transition-colors duration-300 hover-scale">
#                         <i class="fa fa-thumbs-up mr-1.5"></i>
#                         <span>12</span>
#                     </button>
#                     <button class="flex items-center text-neutral-500 hover:text-primary transition-colors duration-300 hover-scale">
#                         <i class="fa fa-comment-o mr-1.5"></i>
#                         <span>4</span>
#                     </button>
#                 </div>
#                 <a href="{{ url_for('forum.view_post', post_id=post._id) }}" class="mt-4 inline-flex items-center text-primary hover:text-primary/80 font-medium transition-colors duration-300 hover-scale">
#                     Read more
#                     <i class="fa fa-arrow-right ml-1.5 text-sm"></i>
#                 </a>
#             </div>
#         </div>
#         {% else %}
#         <div class="bg-white rounded-2xl shadow-card p-8 text-center fade-in">
#             <div class="mb-6 text-5xl text-neutral-300">
#                 <i class="fa fa-comments-o"></i>
#             </div>
#             <h3 class="text-xl md:text-2xl font-semibold text-neutral-800 mb-3">No posts found</h3>
#             <p class="text-neutral-600 mb-8 max-w-md mx-auto">There are no posts matching your criteria. Be the first to start a discussion!</p>
#             <a href="{{ url_for('forum.create_post') }}" class="inline-flex items-center px-6 py-3 bg-primary hover:bg-primary/90 text-white font-medium rounded-lg shadow transition-all btn-pulse">
#                 <i class="fa fa-plus mr-2"></i> Create New Post
#             </a>
#         </div>
#         {% endfor %}
#     </div>
#
#     <!-- 分页导航 -->
#     {% if pagination.total_pages > 1 %}
#     <nav class="mt-12 flex justify-center fade-in">
#         <ul class="inline-flex rounded-md shadow-sm">
#             <!-- 上一页按钮 -->
#             <li>
#                 <a href="{{ build_url(1) }}" class="relative inline-flex items-center px-4 py-2.5 rounded-l-md border border-neutral-300 bg-white text-sm font-medium text-neutral-500 hover:bg-neutral-50 transition-colors duration-300">
#                     <span class="sr-only">First page</span>
#                     <i class="fa fa-angle-double-left"></i>
#                 </a>
#             </li>
#             <li>
#                 <a href="{{ build_url(pagination.page - 1) }}" class="relative inline-flex items-center px-4 py-2.5 border border-neutral-300 bg-white text-sm font-medium text-neutral-500 hover:bg-neutral-50 transition-colors duration-300">
#                     <span class="sr-only">Previous page</span>
#                     <i class="fa fa-angle-left"></i>
#                 </a>
#             </li>
#
#             <!-- 页码范围显示优化 -->
#             {% set start_page = max(1, pagination.page - 2) %}
#             {% set end_page = min(pagination.total_pages, pagination.page + 2) %}
#
#             {% if start_page > 1 %}
#                 <li>
#                     <span class="relative inline-flex items-center px-4 py-2.5 border border-neutral-300 bg-white text-sm font-medium text-neutral-500">
#                         ...
#                     </span>
#                 </li>
#             {% endif %}
#
#             {% for p in range(start_page, end_page + 1) %}
#                 <li>
#                     <a href="{{ build_url(p) }}" class="relative inline-flex items-center px-4 py-2.5 border border-neutral-300 bg-white text-sm font-medium {% if p == pagination.page %}bg-primary text-white border-primary{% else %}text-neutral-700 hover:bg-neutral-50{% endif %} transition-colors duration-300">
#                         {{ p }}
#                     </a>
#                 </li>
#             {% endfor %}
#
#             {% if end_page < pagination.total_pages %}
#                 <li>
#                     <span class="relative inline-flex items-center px-4 py-2.5 border border-neutral-300 bg-white text-sm font-medium text-neutral-500">
#                         ...
#                     </span>
#                 </li>
#             {% endif %}
#
#             <!-- 下一页按钮 -->
#             <li>
#                 <a href="{{ build_url(pagination.page + 1) }}" class="relative inline-flex items-center px-4 py-2.5 border border-neutral-300 bg-white text-sm font-medium text-neutral-500 hover:bg-neutral-50 transition-colors duration-300">
#                     <span class="sr-only">Next page</span>
#                     <i class="fa fa-angle-right"></i>
#                 </a>
#             </li>
#             <li>
#                 <a href="{{ build_url(pagination.total_pages) }}" class="relative inline-flex items-center px-4 py-2.5 rounded-r-md border border-neutral-300 bg-white text-sm font-medium text-neutral-500 hover:bg-neutral-50 transition-colors duration-300">
#                     <span class="sr-only">Last page</span>
#                     <i class="fa fa-angle-double-right"></i>
#                 </a>
#             </li>
#         </ul>
#     </nav>
#     <div class="text-center text-neutral-500 text-sm mt-4 fade-in">
#         Showing {{ posts|length }} of {{ pagination.total }} posts
#         (Page {{ pagination.page }} of {{ pagination.total_pages }})
#     </div>
#     {% endif %}
# </div>
# {% endblock %}
#
# {% block scripts %}
#     {{ super() }}
#     <script>
#         // 日期输入框增强
#         document.addEventListener('DOMContentLoaded', function() {
#             // 初始化日期输入框
#             const dateInputs = document.querySelectorAll('.search-form input[type="date"]');
#             dateInputs.forEach(input => {
#                 // 默认显示为文本类型
#                 if (!input.value) input.type = 'text';
#
#                 input.addEventListener('focus', function() {
#                     this.type = 'date';
#                     if (!this.value) {
#                         // 默认选择今天
#                         const today = new Date().toISOString().split('T')[0];
#                         this.value = today;
#                     }
#                 });
#
#                 input.addEventListener('blur', function() {
#                     if (!this.value) {
#                         this.type = 'text';
#                     }
#                 });
#             });
#
#             // 清除搜索条件
#             const clearFilters = document.createElement('button');
#             clearFilters.className = 'mt-2 text-sm text-primary hover:underline btn-pulse';
#             clearFilters.innerHTML = '<i class="fa fa-times mr-1"></i> Clear filters';
#             clearFilters.addEventListener('click', function(e) {
#                 e.preventDefault();
#                 document.getElementById('keyword').value = '';
#                 document.getElementById('author_id').value = '';
#                 document.getElementById('start_date').value = '';
#                 document.getElementById('end_date').value = '';
#                 document.querySelector('form').submit();
#             });
#             const searchCard = document.querySelector('.search-card');
#             if (searchCard) {
#                 searchCard.querySelector('.card-body').appendChild(clearFilters);
#             }
#
#             // 为帖子卡片添加淡入动画
#             const postCards = document.querySelectorAll('.fade-in');
#             postCards.forEach((card, index) => {
#                 card.style.opacity = '0';
#                 card.style.transform = 'translateY(20px)';
#                 card.style.animationDelay = `${index * 0.1}s`;
#
#                 setTimeout(() => {
#                     card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
#                     card.style.opacity = '1';
#                     card.style.transform = 'translateY(0)';
#                 }, 50 * index);
#             });
#
#             // 导航栏滚动效果
#             const nav = document.querySelector('nav');
#             if (nav) {
#                 window.addEventListener('scroll', function() {
#                     if (window.scrollY > 10) {
#                         nav.classList.add('nav-scrolled', 'shadow-nav');
#                     } else {
#                         nav.classList.remove('nav-scrolled', 'shadow-nav');
#                     }
#                 });
#             }
#         });
#     </script>
# {% endblock %}



# base.html
# <!--<!DOCTYPE html>-->
# <!--<html>-->
# <!--<head>-->
# <!--    <title>{% block title %}Forum{% endblock %}</title>-->
# <!--    <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">-->
# <!--</head>-->
# <!--<body>-->
# <!--    <nav>-->
# <!--        <a href="{{ url_for('forum.index') }}">Home</a>-->
# <!--        <a href="{{ url_for('analysis.dashboard') }}">Analytics</a>-->
# <!--        <a href="{{ url_for('auth.login') }}">Login</a>-->
# <!--    </nav>-->
# <!--    {% for message in get_flashed_messages() %}-->
# <!--        <div class="flash">{{ message }}</div>-->
# <!--    {% endfor %}-->
# <!--    {% block content %}{% endblock %}-->
# <!--</body>-->
# <!--</html>-->


# 新index.html
# {% extends "base.html" %}
# {% macro render_pagination(pagination) %}
# <!-- app/templates/macros/pagination.html -->
# {% macro render_pagination(pagination, endpoint) %}
#   <nav aria-label="Page navigation">
#     <ul class="pagination justify-content-center">
#       {% if pagination.has_prev %}
#         <li class="page-item">
#           <a class="page-link" href="{{ url_for(endpoint, page=pagination.prev_num, **kwargs) }}">
#             &laquo;
#           </a>
#         </li>
#       {% else %}
#         <li class="page-item disabled">
#           <span class="page-link">&laquo;</span>
#         </li>
#       {% endif %}
#       {%- for page in pagination.iter_pages() %}
#         {% if page %}
#           {% if page != pagination.page %}
#             <li class="page-item">
#               <a class="page-link" href="{{ url_for(endpoint, page=page, **kwargs) }}">{{ page }}</a>
#             </li>
#           {% else %}
#             <li class="page-item active">
#               <span class="page-link">{{ page }}</span>
#             </li>
#           {% endif %}
#         {% else %}
#           <li class="page-item disabled">
#             <span class="page-link">...</span>
#           </li>
#         {% endif %}
#       {%- endfor %}
#       {% if pagination.has_next %}
#         <li class="page-item">
#           <a class="page-link" href="{{ url_for(endpoint, page=pagination.next_num, **kwargs) }}">
#             &raquo;
#           </a>
#         </li>
#       {% else %}
#         <li class="page-item disabled">
#           <span class="page-link">&raquo;</span>
#         </li>
#       {% endif %}
#     </ul>
#   </nav>
# {% endmacro %}
# {% endmacro %}
# {% block head %}
#     {{ super() }}
#     <!-- 引入Tailwind CSS -->
#     <script src="https://cdn.tailwindcss.com"></script>
#     <!-- 引入Font Awesome -->
#     <link href="https://cdn.jsdelivr.net/npm/font-awesome@4.7.0/css/font-awesome.min.css" rel="stylesheet">
#
#     <!-- 自定义Tailwind配置 -->
#     <script>
#         tailwind.config = {
#             theme: {
#                 extend: {
#                     colors: {
#                         primary: '#165DFF',
#                         secondary: '#36D399',
#                         neutral: {
#                             100: '#F9FAFB',
#                             200: '#F3F4F6',
#                             300: '#E5E7EB',
#                             400: '#D1D5DB',
#                             500: '#9CA3AF',
#                             600: '#6B7280',
#                             700: '#4B5563',
#                             800: '#1F2937',
#                             900: '#111827',
#                         },
#                     },
#                     fontFamily: {
#                         inter: ['Inter', 'system-ui', 'sans-serif'],
#                     },
#                     boxShadow: {
#                         'card': '0 10px 25px -5px rgba(0, 0, 0, 0.05)',
#                         'card-hover': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
#                         'nav': '0 2px 10px rgba(0, 0, 0, 0.05)',
#                     },
#                     animation: {
#                         'bounce-subtle': 'bounceSubtle 2s infinite',
#                     },
#                     keyframes: {
#                         bounceSubtle: {
#                             '0%, 100%': { transform: 'translateY(0)' },
#                             '50%': { transform: 'translateY(-2px)' },
#                         }
#                     }
#                 },
#             }
#         }
#     </script>
#
#     <!-- 自定义工具类 -->
#     <style type="text/tailwindcss">
#         @layer utilities {
#             .content-auto {
#                 content-visibility: auto;
#             }
#             .author-info {
#                 @apply flex items-center text-sm text-neutral-600;
#             }
#             .post-meta {
#                 @apply flex flex-wrap gap-3 mt-2 text-sm text-neutral-500;
#             }
#             .action-buttons {
#                 @apply flex gap-2 mt-4;
#             }
#             .hover-scale {
#                 @apply transition-transform duration-300 hover:scale-105;
#             }
#         }
#     </style>
#
#     <style>
#         @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
#
#         ::-webkit-scrollbar {
#             width: 8px;
#             height: 8px;
#         }
#         ::-webkit-scrollbar-track {
#             background: #f1f1f1;
#             border-radius: 4px;
#         }
#         ::-webkit-scrollbar-thumb {
#             background: #d1d5db;
#             border-radius: 4px;
#         }
#         ::-webkit-scrollbar-thumb:hover {
#             background: #9ca3af;
#         }
#
#         .fade-in {
#             animation: fadeIn 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards;
#         }
#         @keyframes fadeIn {
#             from { opacity: 0; transform: translateY(15px); }
#             to { opacity: 1; transform: translateY(0); }
#         }
#
#         .nav-scrolled {
#             background-color: rgba(255, 255, 255, 0.95);
#             backdrop-filter: blur(8px);
#             transition: background-color 0.3s, box-shadow 0.3s;
#         }
#     </style>
# {% endblock %}
#
# {% block content %}
# {{ render_pagination(pagination) }}
# <div class="container mx-auto px-4 py-8 max-w-7xl">
#     <!-- 标题和新建按钮 -->
#     <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 fade-in">
#         <div>
#             <h1 class="text-[clamp(1.8rem,3vw,2.5rem)] font-bold text-neutral-800 mb-2 flex items-center">
#                 <i class="fa fa-comments text-primary mr-3 text-[clamp(1.8rem,3vw,2.5rem)] animate-bounce-subtle"></i>
#                 Community Forum
#             </h1>
#             <p class="text-neutral-600 text-lg max-w-2xl text-balance">Join the discussion and share your thoughts with our vibrant community</p>
#         </div>
#         <a href="{{ url_for('forum.create_post') }}"
#            class="mt-4 md:mt-0 bg-primary hover:bg-primary/90 text-white font-medium px-6 py-3 rounded-lg shadow-lg hover:shadow-xl btn-pulse flex items-center">
#             <i class="fa fa-plus mr-2"></i> New Post
#         </a>
#     </div>
#
#     <!-- 搜索面板 -->
#     <div class="bg-white rounded-2xl shadow-card p-6 md:p-8 mb-8 transition-all duration-300 hover-lift fade-in">
#         <form method="get" action="{{ url_for('forum.index') }}" class="space-y-6">
#             <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
#                 <!-- 关键词搜索 -->
#                 <div>
#                     <label for="keyword" class="block text-sm font-medium text-neutral-700 mb-2">Search</label>
#                     <div class="relative">
#                         <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-neutral-500">
#                             <i class="fa fa-search"></i>
#                         </span>
#                         <input type="text" id="keyword" name="keyword" class="w-full pl-10 pr-4 py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary/50 focus:border-primary outline-none transition-all"
#                                placeholder="Search posts by title or content..." value="{{ search_params.keyword }}">
#                     </div>
#                 </div>
#
#                 <!-- 作者筛选 -->
#                 <div>
#                     <label for="author_id" class="block text-sm font-medium text-neutral-700 mb-2">Author</label>
#                     <div class="relative">
#                         <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-neutral-500">
#                             <i class="fa fa-user"></i>
#                         </span>
#                         <input type="text" id="author_id" name="author_id" class="w-full pl-10 pr-4 py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary/50 focus:border-primary outline-none transition-all"
#                                placeholder="Enter author ID or username" value="{{ search_params.author_id }}">
#                     </div>
#                 </div>
#
#                 <!-- 日期范围 -->
#                 <div>
#                     <div class="flex justify-between items-center mb-2">
#                         <label for="start_date" class="block text-sm font-medium text-neutral-700">Start Date</label>
#                         <label for="end_date" class="block text-sm font-medium text-neutral-700">End Date</label>
#                     </div>
#                     <div class="grid grid-cols-2 gap-3">
#                         <div class="relative">
#                             <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-neutral-500">
#                                 <i class="fa fa-calendar"></i>
#                             </span>
#                             <input type="date" id="start_date" name="start_date" class="w-full pl-10 pr-4 py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary/50 focus:border-primary outline-none transition-all"
#                                    value="{{ search_params.start_date }}" placeholder="Start date">
#                         </div>
#                         <div class="relative">
#                             <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-neutral-500">
#                                 <i class="fa fa-calendar"></i>
#                             </span>
#                             <input type="date" id="end_date" name="end_date" class="w-full pl-10 pr-4 py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary/50 focus:border-primary outline-none transition-all"
#                                    value="{{ search_params.end_date }}" placeholder="End date">
#                         </div>
#                     </div>
#                 </div>
#
#                 <!-- 操作按钮 -->
#                 <div class="flex items-end">
#                     <button type="submit" class="w-full bg-primary hover:bg-primary/90 text-white font-medium px-6 py-3 rounded-lg shadow transition-all duration-300 flex items-center justify-center btn-pulse">
#                         <i class="fa fa-filter mr-2"></i> Filter Results
#                     </button>
#                 </div>
#             </div>
#         </form>
#     </div>
#
#     <!-- 帖子列表 -->
#     <div class="space-y-6">
#         {% for post in posts %}
#         <div class="bg-white rounded-2xl shadow-card p-6 md:p-8 hover-lift fade-in" style="animation-delay: {{ loop.index * 0.1 }}s">
#             <!-- 帖子头部：标题和用户信息 -->
#             <div class="mb-6">
#                 <h3 class="text-xl md:text-2xl font-semibold text-neutral-800 mb-2">
#                     <a href="{{ url_for('forum.view_post', post_id=post._id) }}" class="hover:text-primary transition-colors duration-300">
#                         {{ post.title }}
#                     </a>
#                     {% if post.created_at.date() == datetime.utcnow().date() %}
#                     <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800 ml-2 animate-pulse">
#                         <i class="fa fa-circle text-green-500 text-[8px] mr-1"></i> New
#                     </span>
#                     {% endif %}
#                 </h3>
#
#                 <!-- 用户名在左侧，操作按钮在右侧（小屏幕下堆叠） -->
#                 <div class="flex flex-col md:flex-row md:items-center justify-between">
#                     <div class="author-info">
#                         <i class="fa fa-user-circle-o mr-1.5 text-neutral-500"></i>
#                         <a href="{{ url_for('forum.index', author_id=post.author_id) }}" class="text-primary hover:underline transition-colors">
#                             {{ post.author_id|truncate(10) }}
#                         </a>
#                         <span class="mx-2.5 text-neutral-400">•</span>
#                         <i class="fa fa-clock-o mr-1.5 text-neutral-500"></i>
#                         {{ post.created_at.strftime("%Y-%m-%d %H:%M") }}
#                         {% if post.updated_at %}
#                             <span class="mx-2.5 text-neutral-400">•</span>
#                             <span class="text-neutral-500">Updated: {{ post.updated_at.strftime("%Y-%m-%d") }}</span>
#                         {% endif %}
#                     </div>
#
#                     <!-- 删除按钮放在下方（小屏幕）或右侧（大屏幕） -->
#                     {% if post.author_id == current_user_id %}
#                     <div class="mt-3 md:mt-0">
#                         <div class="dropdown relative">
#                             <button class="btn btn-sm btn-outline-secondary dropdown-toggle"
#                                     type="button" data-bs-toggle="dropdown" aria-expanded="false">
#                                 <i class="fa fa-ellipsis-v text-neutral-500"></i>
#                             </button>
#                             <ul class="dropdown-menu absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg py-1 z-10 border-0">
#                                 <li>
#                                     <form action="{{ url_for('forum.delete_post', post_id=post._id) }}"
#                                           method="POST" class="d-inline">
#                                         <button type="submit" class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
#                                                 onclick="return confirm('Delete this post permanently? This action cannot be undone.')">
#                                             <i class="fa fa-trash mr-2 text-red-500"></i> Delete Post
#                                         </button>
#                                     </form>
#                                 </li>
#                             </ul>
#                         </div>
#                     </div>
#                     {% endif %}
#                 </div>
#             </div>
#
#             <!-- 帖子内容：显示在用户名下方/右侧 -->
#             <p class="text-neutral-700 mb-6 leading-relaxed">
#                 {{ post.content|truncate(200) }}
#             </p>
#
#             <!-- 标签展示 -->
#             {% if post.tags %}
#             <div class="flex flex-wrap gap-2 mb-6">
#                 {% for tag in post.tags %}
#                 <span class="inline-flex items-center px-3.5 py-1.5 rounded-full text-sm font-medium bg-neutral-100 text-neutral-700 hover:bg-primary hover:text-white transition-colors duration-300">
#                     <i class="fa fa-tag mr-1.5 text-neutral-500"></i>{{ tag }}
#                 </span>
#                 {% endfor %}
#             </div>
#             {% endif %}
#
#             <!-- 底部交互区：点赞、评论和阅读更多 -->
#             <div class="pt-6 border-t border-neutral-100">
#                 <div class="action-buttons">
#                     <button class="flex items-center text-neutral-500 hover:text-primary transition-colors duration-300 hover-scale">
#                         <i class="fa fa-thumbs-up mr-1.5"></i>
#                         <span>12</span>
#                     </button>
#                     <button class="flex items-center text-neutral-500 hover:text-primary transition-colors duration-300 hover-scale">
#                         <i class="fa fa-comment-o mr-1.5"></i>
#                         <span>4</span>
#                     </button>
#                 </div>
#                 <a href="{{ url_for('forum.view_post', post_id=post._id) }}" class="mt-4 inline-flex items-center text-primary hover:text-primary/80 font-medium transition-colors duration-300 hover-scale">
#                     Read more
#                     <i class="fa fa-arrow-right ml-1.5 text-sm"></i>
#                 </a>
#             </div>
#         </div>
#         {% else %}
#         <div class="bg-white rounded-2xl shadow-card p-8 text-center fade-in">
#             <div class="mb-6 text-5xl text-neutral-300">
#                 <i class="fa fa-comments-o"></i>
#             </div>
#             <h3 class="text-xl md:text-2xl font-semibold text-neutral-800 mb-3">No posts found</h3>
#             <p class="text-neutral-600 mb-8 max-w-md mx-auto">There are no posts matching your criteria. Be the first to start a discussion!</p>
#             <a href="{{ url_for('forum.create_post') }}" class="inline-flex items-center px-6 py-3 bg-primary hover:bg-primary/90 text-white font-medium rounded-lg shadow transition-all btn-pulse">
#                 <i class="fa fa-plus mr-2"></i> Create New Post
#             </a>
#         </div>
#         {% endfor %}
#     </div>
#
#     <!-- 分页导航 -->
#     {% if pagination.total_pages > 1 %}
#     <nav class="mt-12 flex justify-center fade-in">
#         <ul class="inline-flex rounded-md shadow-sm">
#             <!-- 上一页按钮 -->
#             <li>
#                 <a href="{{ build_url(1) }}" class="relative inline-flex items-center px-4 py-2.5 rounded-l-md border border-neutral-300 bg-white text-sm font-medium text-neutral-500 hover:bg-neutral-50 transition-colors duration-300">
#                     <span class="sr-only">First page</span>
#                     <i class="fa fa-angle-double-left"></i>
#                 </a>
#             </li>
#             <li>
#                 <a href="{{ build_url(pagination.page - 1) }}" class="relative inline-flex items-center px-4 py-2.5 border border-neutral-300 bg-white text-sm font-medium text-neutral-500 hover:bg-neutral-50 transition-colors duration-300">
#                     <span class="sr-only">Previous page</span>
#                     <i class="fa fa-angle-left"></i>
#                 </a>
#             </li>
#
#             <!-- 页码范围显示优化 -->
#             {% set start_page = max(1, pagination.page - 2) %}
#             {% set end_page = min(pagination.total_pages, pagination.page + 2) %}
#
#             {% if start_page > 1 %}
#                 <li>
#                     <span class="relative inline-flex items-center px-4 py-2.5 border border-neutral-300 bg-white text-sm font-medium text-neutral-500">
#                         ...
#                     </span>
#                 </li>
#             {% endif %}
#
#             {% for p in range(start_page, end_page + 1) %}
#                 <li>
#                     <a href="{{ build_url(p) }}" class="relative inline-flex items-center px-4 py-2.5 border border-neutral-300 bg-white text-sm font-medium {% if p == pagination.page %}bg-primary text-white border-primary{% else %}text-neutral-700 hover:bg-neutral-50{% endif %} transition-colors duration-300">
#                         {{ p }}
#                     </a>
#                 </li>
#             {% endfor %}
#
#             {% if end_page < pagination.total_pages %}
#                 <li>
#                     <span class="relative inline-flex items-center px-4 py-2.5 border border-neutral-300 bg-white text-sm font-medium text-neutral-500">
#                         ...
#                     </span>
#                 </li>
#             {% endif %}
#
#             <!-- 下一页按钮 -->
#             <li>
#                 <a href="{{ build_url(pagination.page + 1) }}" class="relative inline-flex items-center px-4 py-2.5 border border-neutral-300 bg-white text-sm font-medium text-neutral-500 hover:bg-neutral-50 transition-colors duration-300">
#                     <span class="sr-only">Next page</span>
#                     <i class="fa fa-angle-right"></i>
#                 </a>
#             </li>
#             <li>
#                 <a href="{{ build_url(pagination.total_pages) }}" class="relative inline-flex items-center px-4 py-2.5 rounded-r-md border border-neutral-300 bg-white text-sm font-medium text-neutral-500 hover:bg-neutral-50 transition-colors duration-300">
#                     <span class="sr-only">Last page</span>
#                     <i class="fa fa-angle-double-right"></i>
#                 </a>
#             </li>
#         </ul>
#     </nav>
#     <div class="text-center text-neutral-500 text-sm mt-4 fade-in">
#         Showing {{ posts|length }} of {{ pagination.total }} posts
#         (Page {{ pagination.page }} of {{ pagination.total_pages }})
#     </div>
#     {% endif %}
# </div>
# {% endblock %}
#
# {% block scripts %}
#     {{ super() }}
#     <script>
#         // 日期输入框增强
#         document.addEventListener('DOMContentLoaded', function() {
#             // 初始化日期输入框
#             const dateInputs = document.querySelectorAll('.search-form input[type="date"]');
#             dateInputs.forEach(input => {
#                 // 默认显示为文本类型
#                 if (!input.value) input.type = 'text';
#
#                 input.addEventListener('focus', function() {
#                     this.type = 'date';
#                     if (!this.value) {
#                         // 默认选择今天
#                         const today = new Date().toISOString().split('T')[0];
#                         this.value = today;
#                     }
#                 });
#
#                 input.addEventListener('blur', function() {
#                     if (!this.value) {
#                         this.type = 'text';
#                     }
#                 });
#             });
#
#             // 清除搜索条件
#             const clearFilters = document.createElement('button');
#             clearFilters.className = 'mt-2 text-sm text-primary hover:underline btn-pulse';
#             clearFilters.innerHTML = '<i class="fa fa-times mr-1"></i> Clear filters';
#             clearFilters.addEventListener('click', function(e) {
#                 e.preventDefault();
#                 document.getElementById('keyword').value = '';
#                 document.getElementById('author_id').value = '';
#                 document.getElementById('start_date').value = '';
#                 document.getElementById('end_date').value = '';
#                 document.querySelector('form').submit();
#             });
#             const searchCard = document.querySelector('.search-card');
#             if (searchCard) {
#                 searchCard.querySelector('.card-body').appendChild(clearFilters);
#             }
#
#             // 为帖子卡片添加淡入动画
#             const postCards = document.querySelectorAll('.fade-in');
#             postCards.forEach((card, index) => {
#                 card.style.opacity = '0';
#                 card.style.transform = 'translateY(20px)';
#                 card.style.animationDelay = `${index * 0.1}s`;
#
#                 setTimeout(() => {
#                     card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
#                     card.style.opacity = '1';
#                     card.style.transform = 'translateY(0)';
#                 }, 50 * index);
#             });
#
#             // 导航栏滚动效果
#             const nav = document.querySelector('nav');
#             if (nav) {
#                 window.addEventListener('scroll', function() {
#                     if (window.scrollY > 10) {
#                         nav.classList.add('nav-scrolled', 'shadow-nav');
#                     } else {
#                         nav.classList.remove('nav-scrolled', 'shadow-nav');
#                     }
#                 });
#             }
#         });
#     </script>
# {% endblock %}


# login.html
# {% extends "base.html" %}
# {% block styles %}
# <style>
#     .login-form {
#         max-width: 400px;
#         margin: 0 auto;
#         padding: 2rem;
#         background-color: white;
#         border-radius: 0.5rem;
#         box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
#     }
#
#     .login-form label {
#         display: block;
#         margin-bottom: 0.5rem;
#         font-weight: 500;
#     }
#
#     .login-form input {
#         width: 100%;
#         padding: 0.75rem;
#         margin-bottom: 1rem;
#         border: 1px solid #ddd;
#         border-radius: 0.25rem;
#     }
#
#     .login-form button {
#         width: 100%;
#         padding: 0.75rem;
#         background-color: #3b82f6;
#         color: white;
#         border: none;
#         border-radius: 0.25rem;
#         cursor: pointer;
#     }
#
#     .register-link {
#         display: block;
#         text-align: center;
#         margin-top: 1rem;
#     }
# </style>
# {% endblock %}
# {% block content %}
# <h2>Login</h2>
# <form method="POST">
#     <div>
#         <label>Username:</label>
#         <input type="text" name="username" required>
#     </div>
#     <div>
#         <label>Password:</label>
#         <input type="password" name="password" required>
#     </div>
#     <button type="submit">Login</button>
# </form>
# <a href="{{ url_for('auth.register') }}">Register</a>
# {% endblock %}


# dashboard.html
# {% extends "base.html" %}
# {% block head %}
#     {{ super() }}
#     <link rel="stylesheet" href="{{ url_for('static', filename='css/forum.css') }}">
# {% endblock %}
# {% block content %}
# <h1>Analytics Dashboard</h1>
# <div class="chart-container">
#     <h3>Posts per User</h3>
#     <ul>
#         {% for stat in post_stats %}
#         <li>User {{ stat._id }}: {{ stat.count }} posts</li>
#         {% endfor %}
#     </ul>
# </div>
# {% endblock %}