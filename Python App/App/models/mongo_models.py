# from datetime import datetime
# from bson import ObjectId
# from App.extensions import mongo
# from App.extensions import db
# from flask import current_app
# class Post:
#     @staticmethod
#     def get_collection():
#         return mongo.db.posts
#
#     @classmethod
#     def create(cls, data):
#         data['created_at'] = datetime.utcnow()
#         return cls.get_collection().insert_one(data).inserted_id
#     @classmethod
#     def delete(cls, post_id):
#         return cls.get_collection().delete_one({'_id': ObjectId(post_id)})
#     @classmethod
#     def update(cls, post_id, data):
#         return cls.get_collection().update_one(
#             {'_id': ObjectId(post_id)},
#             {'$set': data}
#         )
#     @classmethod
#     def find_all(cls, query={}, sort_by='created_at', limit=20):
#         return list(cls.get_collection().find(query)
#                    .sort(sort_by, -1).limit(limit))


from datetime import datetime
from bson import ObjectId
from App.extensions import mongo
from flask import current_app


class Post:
    @staticmethod
    def get_collection():
        """获取 MongoDB 集合对象"""
        return mongo.db.posts

    @classmethod
    def create(cls, data):
        """创建新帖子"""
        if 'created_at' not in data:
            data['created_at'] = datetime.utcnow()
        result = cls.get_collection().insert_one(data)
        return str(result.inserted_id)

    @classmethod
    def delete(cls, post_id):
        """删除帖子"""
        if not ObjectId.is_valid(post_id):
            return None
        return cls.get_collection().delete_one({'_id': ObjectId(post_id)})

    @classmethod
    def update(cls, post_id, data):
        """更新帖子"""
        if not ObjectId.is_valid(post_id):
            return None
        data['updated_at'] = datetime.utcnow()
        return cls.get_collection().update_one(
            {'_id': ObjectId(post_id)},
            {'$set': data}
        )

    @classmethod
    def find_by_id(cls, post_id):
        """通过 ID 获取单条帖子"""
        if not ObjectId.is_valid(post_id):
            return None
        post = cls.get_collection().find_one({'_id': ObjectId(post_id)})
        if post:
            post['_id'] = str(post['_id'])
        return post

    @staticmethod
    def increment_view_count(post_id):
        """增加帖子浏览计数"""
        mongo.db.posts.update_one(
            {'_id': ObjectId(post_id)},
            {'$inc': {'view_count': 1}})

    @classmethod
    def find_with_pagination(
            cls,
            query_conditions=None,
            page=1,
            per_page=10,
            sort_field='created_at',
            sort_order=-1,
            projection=None
    ):
        """增强版分页查询"""
        try:
            if query_conditions is None:
                query_conditions = {}

            collection = cls.get_collection()
            skip = (page - 1) * per_page

            # 执行查询并转换ObjectId为字符串
            cursor = collection.find(query_conditions, projection) \
                .sort(sort_field, sort_order) \
                .skip(skip) \
                .limit(per_page)

            items = []
            for item in cursor:
                item['_id'] = str(item['_id'])  # 转换ObjectId为字符串
                items.append(item)

            # 获取总数
            total = collection.count_documents(query_conditions)

            return {
                'items': items,
                'total': total,
                'page': page,
                'per_page': per_page,
                'total_pages': max(1, (total + per_page - 1) // per_page)
            }
        except Exception as e:
            current_app.logger.error(f"MongoDB query error: {str(e)}")
            return {
                'items': [],
                'total': 0,
                'page': 1,
                'per_page': per_page,
                'total_pages': 1
            }


