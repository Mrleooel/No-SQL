import os
from App import create_app
from App.extensions import db, mongo
from App.models.sql_models import User


def initialize_databases():
    app = create_app()

    with app.app_context():
        # Debug: 打印所有关键配置
        print("=== CONFIG DEBUG ===")
        print("MONGO_URI:", app.config.get("MONGO_URI"))  # 必须显示有效URI
        print("MONGO_DB_NAME:", mongo.cx.get_database().name)  # 显示实际连接的数据库
        print("====================")
        try:

            # 1. 初始化SQL数据库
            db.create_all()

            # 2. 初始化MongoDB
            collections = mongo.db.list_collection_names()
            if 'posts' not in collections:
                mongo.db.create_collection('posts')

            # 避免重复创建索引
            if 'title_text' not in mongo.db.posts.index_information():
                mongo.db.posts.create_index([('title', 'text')])
                mongo.db.posts.create_index([('author_id', 1)])

            # 3. 初始化测试数据（含三种角色）
            if not User.query.first():
                users = [
                    User(
                        username='admin',
                        password='admin',
                        role='admin'
                    ),
                    User(
                        username='company_demo',
                        password='company',
                        role='company'
                    ),
                    User(
                        username='user1',
                        password='user',
                        role='user'
                    )
                ]
                db.session.add_all(users)
                db.session.commit()

            print("✅ 数据库初始化成功")
            print(f"SQL Tables: {', '.join(db.metadata.tables.keys())}")
            print(f"MongoDB Collections: {', '.join(mongo.db.list_collection_names())}")

        except Exception as e:
            print(f"❌ 初始化失败: {str(e)}")
            raise


if __name__ == '__main__':
    initialize_databases()