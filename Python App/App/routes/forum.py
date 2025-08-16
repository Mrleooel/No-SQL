# from flask import Blueprint, render_template, request, flash
# from flask_login import login_required, current_user
# from flask import redirect, url_for
# from bson import ObjectId
# from App.models.mongo_models import Post
# bp = Blueprint('forum', __name__)
# @bp.route('/')
# @login_required
# def index():
#     keyword = request.args.get('keyword', '')
#     query = {'title': {'$regex': keyword}} if keyword else {}
#     posts = Post.find_all(query)
#     return render_template('forum/index.html', posts=posts)
# @bp.route('/post/create', methods=['GET', 'POST'])
# @login_required
# def create_post():
#     if request.method == 'POST':
#         post_data = {
#             'title': request.form['title'],
#             'content': request.form['content'],
#             'author_id': str(current_user.id)
#         }
#         Post.create(post_data)
#         flash('Post created successfully!')
#         return redirect(url_for('forum.index'))
#     return render_template('forum/create.html')


from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from bson import ObjectId
from datetime import datetime
from urllib.parse import urlencode
from App.models.mongo_models import Post
import re

bp = Blueprint('forum', __name__)


def build_query_parameters(args):
    """构建查询参数字典"""
    params = {
        'keyword': args.get('keyword', '').strip(),
        'author_id': args.get('author_id', '').strip(),
        'author_name': args.get('author_name', '').strip(),
        'start_date': args.get('start_date'),
        'end_date': args.get('end_date'),
        'page': args.get('page', 1, type=int)
    }
    return {k: v for k, v in params.items() if v}


def validate_dates(start_date, end_date):
    """验证日期格式并返回日期对象或错误消息"""
    date_error = None
    start, end = None, None

    try:
        if start_date:
            start = datetime.strptime(start_date, '%Y-%m-%d')
        if end_date:
            end = datetime.strptime(end_date + ' 23:59:59', '%Y-%m-%d %H:%M:%S')

        # 检查日期范围是否合理
        if start and end and start > end:
            date_error = "End date must be after start date"
    except ValueError:
        date_error = "Invalid date format. Please use YYYY-MM-DD."

    return start, end, date_error


def build_search_query(params):
    """根据参数构建MongoDB查询条件"""
    query = {}

    # 关键词搜索
    if params.get('keyword'):
        query['$or'] = [
            {'title': {'$regex': params['keyword'], '$options': 'i'}},
            {'content': {'$regex': params['keyword'], '$options': 'i'}}
        ]

    # 作者筛选
    if params.get('author_id'):
        query['author_id'] = params['author_id']

    if params.get('author_name'):
        query['author_name'] = params['author_name']

    # 日期范围
    start, end, date_error = validate_dates(params.get('start_date'), params.get('end_date'))
    if date_error:
        flash(date_error, 'error')
    else:
        if start:
            query.setdefault('created_at', {})['$gte'] = start
        if end:
            query.setdefault('created_at', {})['$lte'] = end

    return query





@bp.route('/')
@login_required
def index():
    # 获取并处理查询参数
    params = build_query_parameters(request.args)
    page = params.get('page', 1)
    per_page = 10

    # 构建查询条件
    query = build_search_query(params)

    # 执行分页查询
    posts_data = Post.find_with_pagination(
        query_conditions=query,
        page=page,
        per_page=per_page,
        sort_field='created_at',
        sort_order=-1
    )

    # 构建分页URL生成函数
    def build_pagination_url(p):
        new_params = params.copy()
        new_params['page'] = p
        return f"{url_for('forum.index')}?{urlencode(new_params)}"

    return render_template(
        'forum/index.html',
        posts=posts_data['items'],
        pagination=posts_data,
        build_url=build_pagination_url,
        search_params=params,
        current_user_id=str(current_user.id)
    )


@bp.route('/post/<post_id>')
@login_required
def view_post(post_id):
    post = Post.find_by_id(post_id)
    if not post:
        flash('Post not found', 'error')
        return redirect(url_for('forum.index'))

    # 记录浏览量 (可选实现)
    Post.increment_view_count(post_id)

    return render_template('forum/post.html', post=post)


@bp.route('/post/create', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        # 验证必填字段
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        if not title or not content:
            flash('Title and content are required', 'error')
            return render_template('forum/create.html',
                                   title=title,
                                   content=content,
                                   tags=request.form.get('tags', ''))

        # 创建新帖子
        post_data = {
            'title': title,
            'content': content,
            'author_id': str(current_user.id),
            'author_name': current_user.username,
            'tags': [tag.strip() for tag in request.form.get('tags', '').split(',') if tag.strip()],
            'view_count': 0
        }

        try:
            post_id = Post.create(post_data)
            flash('Post created successfully!', 'success')
            return redirect(url_for('forum.view_post', post_id=post_id))
        except Exception as e:
            current_app.logger.error(f"Failed to create post: {str(e)}")
            flash('Failed to create post. Please try again.', 'error')

    return render_template('forum/create.html')


@bp.route('/post/<post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.find_by_id(post_id)
    if not post:
        flash('Post not found', 'error')
        return redirect(url_for('forum.index'))

    # 权限验证
    if post['author_id'] != str(current_user.id):
        flash('You can only edit your own posts', 'error')
        return redirect(url_for('forum.view_post', post_id=post_id))

    if request.method == 'POST':
        # 验证必填字段
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        if not title or not content:
            flash('Title and content are required', 'error')
            return render_template('forum/edit.html', post=post)

        # 更新帖子
        update_data = {
            'title': title,
            'content': content,
            'tags': [tag.strip() for tag in request.form.get('tags', '').split(',') if tag.strip()],
            'updated_at': datetime.utcnow()
        }

        try:
            Post.update(post_id, update_data)
            flash('Post updated successfully!', 'success')
            return redirect(url_for('forum.view_post', post_id=post_id))
        except Exception as e:
            current_app.logger.error(f"Failed to update post: {str(e)}")
            flash('Failed to update post. Please try again.', 'error')

    return render_template('forum/edit.html', post=post)


@bp.route('/post/<post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.find_by_id(post_id)
    if not post:
        flash('Post not found', 'error')
        return redirect(url_for('forum.index'))

    # 权限验证
    if post['author_id'] != str(current_user.id):
        flash('You can only delete your own posts', 'error')
        return redirect(url_for('forum.view_post', post_id=post_id))

    try:
        Post.delete(post_id)
        flash('Post deleted successfully', 'success')
    except Exception as e:
        current_app.logger.error(f"Failed to delete post: {str(e)}")
        flash('Failed to delete post', 'error')

    return redirect(url_for('forum.index'))


# @bp.route('/posts/user/<user_id>')
# @login_required
# def user_posts(user_id):
#     """查看特定用户的帖子"""
#     params = build_query_parameters(request.args)
#     params['author_id'] = user_id  # 强制添加作者ID条件
#
#     page = params.get('page', 1)
#     per_page = 10
#
#     # 构建查询条件
#     query = build_search_query(params)
#
#     # 执行分页查询
#     posts_data = Post.find_with_pagination(
#         query_conditions=query,
#         page=page,
#         per_page=per_page,
#         sort_field='created_at',
#         sort_order=-1
#     )
#
#     # 构建分页URL
#     def build_pagination_url(p):
#         new_params = params.copy()
#         new_params['page'] = p
#         return f"{url_for('forum.user_posts', user_id=user_id)}?{urlencode(new_params)}"
#
#     return render_template(
#         'forum/index.html',
#         posts=posts_data['items'],
#         pagination=posts_data,
#         build_url=build_pagination_url,
#         search_params=params,
#         current_user_id=str(current_user.id),
#         viewing_user=user_id
#     )


@bp.route('/posts/user/<identifier>')
@login_required
def user_posts(identifier):
    print(f"开始处理用户帖子请求，标识符: {identifier}")
    try:
        # 构建更可靠的查询条件
        from bson import ObjectId
        query = {}

        # 尝试作为ObjectID查询
        try:
            if ObjectId.is_valid(identifier):
                query['author_id'] = ObjectId(identifier)
            else:
                # 用户名查询 (不区分大小写)
                query['author_name'] = {'$regex': f'^{identifier}$', '$options': 'i'}
        except:
            query['$or'] = [
                {'author_id': identifier},
                {'author_name': {'$regex': f'^{identifier}$', '$options': 'i'}}
            ]
        print(f"最终查询条件: {query}")

        # 执行查询测试
        test_result = list(Post.find(query).limit(1))
        if not test_result:
            print("测试查询返回空结果")

        # 分页查询
        page = request.args.get('page', 1, type=int)
        posts_data = Post.find_with_pagination(
            query_conditions=query,
            page=page,
            per_page=10,
            sort_field='created_at',
            sort_order=-1
        )
        for post in posts_data['items']:
            if 'author_name' not in post:
                post['author_name'] = str(post['author_id'])
                print(f"为post {post['_id']} 添加默认author_name")
    except Exception as e:
        print(f"数据库查询错误: {str(e)}")
        posts_data = {'items': [], 'total': 0, 'pages': 1}
    return render_template(
        'forum/index.html',
        posts=posts_data['items'],
        pagination=posts_data,
        build_url=lambda p: url_for('forum.user_posts', identifier=identifier, page=p),
        current_user_id=str(current_user.id),
        viewing_user=identifier
    )

@bp.context_processor
def inject_datetime():
    return {'datetime': datetime}

