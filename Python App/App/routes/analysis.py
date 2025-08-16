# from flask import Blueprint, render_template
# from flask_login import login_required
# from App.extensions import mongo
# import pandas as pd
# bp = Blueprint('analysis', __name__)
# @bp.route('/dashboard')
# @login_required
# def dashboard():
#     # 获取发帖量统计
#     post_stats = list(mongo.db.posts.aggregate([
#         {'$group': {'_id': '$author_id', 'count': {'$sum': 1}}}
#     ]))
#     df = pd.DataFrame(post_stats)
#     return render_template('analysis/dashboard.html',
#                          post_stats=df.to_dict('records'))


from flask import Blueprint, render_template
from flask_login import login_required
from App.extensions import mongo
import pandas as pd
import matplotlib
import json
from bson import json_util
matplotlib.use('Agg')  # 必须在其他matplotlib导入前设置
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import warnings
plt.rcParams['font.sans-serif'] = ['SimHei']

bp = Blueprint('analysis', __name__)


@bp.route('/dashboard')
@login_required
def dashboard():
    # 获取发帖量统计
    post_stats = list(mongo.db.posts.aggregate([
        {'$group': {'_id': '$author_id', 'count': {'$sum': 1}}}
    ]))

    print(f"Debug - Raw Stats: {post_stats}")  # 调试输出原始数据
    if not post_stats:
        return render_template('analysis/dashboard.html',
                               message="没有找到发帖数据",
                               chart_image=None)
    # # 获取作者信息
    # user_ids = [stat['_id'] for stat in post_stats]
    # users = mongo.db.users.find({'_id': {'$in': user_ids}},{'username': 1})
    # username_map = {user['_id']: user.get('username', f"用户{user['_id']}") for user in users}
    # # 准备图表数据
    # chart_data = []
    # for stat in post_stats:
    #     chart_data.append({
    #         'user_id': stat['_id'],
    #         'username': username_map.get(stat['_id'], f"User{stat['_id']}"),
    #         'count': stat['count']
    #     })
    #
    # print(f"Debug - Chart Data: {chart_data}")  # 调试输出处理后的数据

    pipeline = [
        {"$group": {"_id": "$author_id", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    post_stats = list(mongo.db.posts.aggregate(pipeline))
    chart_data = []
    for stat in post_stats:
        # 获取该 author_id 下的任意一篇帖子（用于提取 author_name）
        sample_post = mongo.db.posts.find_one(
            {"author_id": stat["_id"]},
            {"author_name": 1}
        )
        username = sample_post.get("author_name", f"User{stat['_id']}")
        if isinstance(username, str):
            username = username.encode('utf-8').decode('utf-8')  # 显式UTF-8解码
        chart_data.append({
            "user_id": stat["_id"],
            # "username": sample_post.get("author_name", f"User{stat['_id']}"),
            "username": username,
            "count": stat["count"]
        })
    output = json.dumps(
        chart_data,
        indent=2,
        ensure_ascii=False,
        default=json_util.default
    )
    # print("output"+output)

    # 生成图表
    try:
        img = generate_bar_chart(chart_data)
    except Exception as e:
        print(f"图表生成错误: {str(e)}")
        img = None
    return render_template('analysis/dashboard.html',
                           post_stats=chart_data,
                           chart_image=img)


def generate_bar_chart(data):
    # 过滤无效数据
    valid_data = [d for d in data if isinstance(d['count'], (int, float)) and d['count'] >= 0]
    if not valid_data:
        raise ValueError("没有有效的发帖量数据")

    # 提取图表需要的列
    usernames = [d['username'] for d in valid_data]
    counts = [d['count'] for d in valid_data]
    # 创建图表
    plt.figure(figsize=(10, 6))
    bars = plt.bar(usernames, counts, color='#4e79a7')

    # 添加数据标签
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height,
                 f'{int(height)}',
                 ha='center', va='bottom',
                 fontsize=10)

    # 图表装饰
    plt.title('User posting volume statistics', pad=20)
    plt.xlabel('UserName')
    plt.ylabel('Posting quantity')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # 保存到内存
    buffer = BytesIO()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    plt.close()

    buffer.seek(0)
    return f"data:image/png;base64,{base64.b64encode(buffer.read()).decode()}"