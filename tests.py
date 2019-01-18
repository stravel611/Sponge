# coding: utf-8
import unittest
from app import app
from app.exts import db
from app.models import Category, Item, Record, Tag
from datetime import datetime


BASE_URL = '/api/v1'


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'
        )
        self.context = app.test_request_context()
        self.context.push()
        self.client = app.test_client()

        db.create_all()

    def tearDown(self):
        db.drop_all()
        self.context.pop()


class CategoryTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        category = Category(name='test')
        db.session.add(category)
        db.session.commit()

    def test_category(self):
        """
        api: /category
        methods: get: 获取所有分类
                 post: 创建一个分类
        """
        # 获取所有分类
        res = self.client.get(BASE_URL + '/category').get_json()
        self.assertEqual(res['status'], 200)
        self.assertEqual(res['data'][0]['name'], 'test')

        # 创建一个分类，但未提供参数
        res = self.client.post(BASE_URL + '/category').get_json()
        self.assertEqual(res['status'], 400)

        # 创建一个分类
        res = self.client.post(BASE_URL + '/category', data={'name': 'new_category'}).get_json()
        self.assertEqual(res['status'], 201)
        self.assertEqual(res['data']['name'], 'new_category')
        self.assertEqual(len(Category.query.all()), 2)

    def test_category_member(self):
        """
        api: /category/<int:category_id>
        methods: get: 获取一个分类的详情
                 put: 更新一个分类的信息
                 delete: 删除一个分类
        """
        # 更新一个不存在的分类
        res = self.client.put(BASE_URL + '/category/100').get_json()
        self.assertEqual(res['status'], 404)

        # 更新一个分类，但未提供参数
        res = self.client.put(BASE_URL + '/category/1').get_json()
        self.assertEqual(res['status'], 400)

        # 更新一个分类的名称
        res = self.client.put(BASE_URL + '/category/1', data={'name': 'changed_name'}).get_json()
        self.assertEqual(res['status'], 200)
        self.assertEqual(res['data']['name'], 'changed_name')
        category = Category.query.get(1)
        self.assertEqual(category.name, 'changed_name')

        # 获取一个分类
        res = self.client.get(BASE_URL + '/category/1').get_json()
        self.assertEqual(res['status'], 200)
        self.assertEqual(res['data']['name'], 'changed_name')

        # 删除一个不存在的分类
        res = self.client.delete(BASE_URL + '/category/100').get_json()
        self.assertEqual(res['status'], 404)

        # 删除一个分类
        res = self.client.delete(BASE_URL + '/category/1').get_json()
        self.assertEqual(res['status'], 200)
        category = Category.query.get(1)
        self.assertIsNone(category)

        # 获取一个不存在（已删除）的分类
        res = self.client.get(BASE_URL + '/category/1').get_json()
        self.assertEqual(res['status'], 404)


class ItemTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        category = Category(name='test_category')
        item = Item(name='test_item')
        item.category = category
        db.session.add(item)
        db.session.commit()

    def test_item(self):
        """
        api: /item
        methods: get: 获取所有条目
                 post: 创建一个条目
        """
        # 获取所有条目
        res = self.client.get(BASE_URL + '/item').get_json()
        self.assertEqual(res['status'], 200)
        self.assertEqual(res['data'][0]['name'], 'test_item')

        # 创建一个条目，但未提供参数
        res = self.client.post(BASE_URL + '/item').get_json()
        self.assertEqual(res['status'], 400)

        # 创建一个条目
        res = self.client.post(BASE_URL + '/item', data={'name': 'new_item'}).get_json()
        self.assertEqual(res['status'], 201)
        self.assertEqual(res['data']['name'], 'new_item')
        self.assertEqual(len(Item.query.all()), 2)

    def test_item_member(self):
        """
        api: /item/<int:item_id>
        methods: get: 获取一个条目的详情
                 put: 更新一个条目的信息
                 delete: 删除一个条目
        """
        # 更新一个不存在的条目
        res = self.client.put(BASE_URL + '/item/100').get_json()
        self.assertEqual(res['status'], 404)

        # 更新一个条目，但未提供参数
        res = self.client.put(BASE_URL + '/item/1').get_json()
        self.assertEqual(res['status'], 400)

        # 更新一个条目的名称
        res = self.client.put(BASE_URL + '/item/1', data={'name': 'changed_name'}).get_json()
        self.assertEqual(res['status'], 200)
        self.assertEqual(res['data']['name'], 'changed_name')
        item = Item.query.get(1)
        self.assertEqual(item.name, 'changed_name')

        # 获取一个条目
        res = self.client.get(BASE_URL + '/item/1').get_json()
        self.assertEqual(res['status'], 200)
        self.assertEqual(res['data']['name'], 'changed_name')

        # 删除一个不存在的条目
        res = self.client.delete(BASE_URL + '/item/100').get_json()
        self.assertEqual(res['status'], 404)

        # 删除一个条目
        res = self.client.delete(BASE_URL + '/item/1').get_json()
        self.assertEqual(res['status'], 200)
        item = Item.query.get(1)
        self.assertIsNone(item)

        # 获取一个不存在（已删除）的条目
        res = self.client.get(BASE_URL + '/item/1').get_json()
        self.assertEqual(res['status'], 404)

    def test_item_of_category(self):
        """
        api: /category/<int:category_id>/item
        methods: get: 获取一个分类下的所有条目
                 post: 在一个分类下创建一个条目
        """
        # 获取一个分类下的所有条目
        res = self.client.get(BASE_URL + '/category/1/item').get_json()
        self.assertEqual(res['status'], 200)
        self.assertEqual(res['data'][0]['name'], 'test_item')

        # 在一个分类下创建一个条目，但未提供参数
        res = self.client.post(BASE_URL + '/category/1/item').get_json()
        self.assertEqual(res['status'], 400)

        # 在一个分类下创建一个条目
        res = self.client.post(BASE_URL + '/category/1/item', data={'name': 'new_item'}).get_json()
        self.assertEqual(res['status'], 201)
        self.assertEqual(res['data']['name'], 'new_item')
        category = Category.query.get(1)
        self.assertEqual(len(category.items), 2)


class RecordTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        category = Category(name='test_category')
        item = Item(name='test_item')
        item.category = category
        record_1 = Record(
            start=datetime(2019, 1, 10, 6, 0, 0),
            finish=datetime(2019, 1, 10, 7, 0, 0),
            remark='test_record_1'
        )
        record_2 = Record(
            start=datetime(2019, 1, 11, 6, 0, 0),
            finish=datetime(2019, 1, 11, 7, 0, 0),
            remark='test_record_2'
        )
        item.records = [record_1, record_2]
        db.session.add(item)
        db.session.commit()

    def test_record(self):
        """
        api: /record
        methods: get: 获取所有记录
        """
        # 获取所有记录
        res = self.client.get(BASE_URL + '/record').get_json()
        self.assertEqual(res['status'], 200)
        self.assertEqual(res['data'][0]['remark'], 'test_record_1')
        
    def test_record_member(self):
        """
        api: /record/<int:record_id>
        methods: get: 获取一条记录的详情
                 put: 更新一条记录的信息
                 delete: 删除一条记录
        """
        # 更新一条不存在的记录
        res = self.client.put(BASE_URL + '/record/100').get_json()
        self.assertEqual(res['status'], 404)

        # 更新一条记录，但未提供参数
        res = self.client.put(BASE_URL + '/record/1').get_json()
        self.assertEqual(res['status'], 400)

        # 更新一条记录的结束时间
        new_finish = datetime(2019, 1, 10, 8, 0, 0)
        res = self.client.put(BASE_URL + '/record/1', data={'finish': int(new_finish.timestamp() * 1000)}).get_json()
        self.assertEqual(res['status'], 200)
        self.assertEqual(res['data']['finish'], '2019-01-10T08:00:00')
        record = Record.query.get(1)
        self.assertEqual(record.finish, new_finish)

        # 更新一条记录的备注，但与原内容相同
        res = self.client.put(BASE_URL + '/record/1', data={'remark': 'test_record_1'}).get_json()
        self.assertEqual(res['status'], 409)

        # 更新一条记录的备注
        res = self.client.put(BASE_URL + '/record/1', data={'remark': 'changed_remark'}).get_json()
        self.assertEqual(res['status'], 200)
        self.assertEqual(res['data']['remark'], 'changed_remark')
        record = Record.query.get(1)
        self.assertEqual(record.remark, 'changed_remark')

        # 获取一条记录
        res = self.client.get(BASE_URL + '/record/1').get_json()
        self.assertEqual(res['status'], 200)
        self.assertEqual(res['data']['remark'], 'changed_remark')

        # 删除一条不存在的记录
        res = self.client.delete(BASE_URL + '/record/100').get_json()
        self.assertEqual(res['status'], 404)

        # 删除一条记录
        res = self.client.delete(BASE_URL + '/record/1').get_json()
        self.assertEqual(res['status'], 200)
        record = Record.query.get(1)
        self.assertIsNone(record)

        # 获取一条不存在（已删除）的记录
        res = self.client.get(BASE_URL + '/record/1').get_json()
        self.assertEqual(res['status'], 404)
        
    def test_record_of_category(self):
        """
        api: /category/<int:category_id>/record
        methods: get: 获取一个分类下的所有记录
        """
        # 获取一个分类下的所有记录
        res = self.client.get(BASE_URL + '/category/1/record').get_json()
        self.assertEqual(res['status'], 200)
        self.assertEqual(len(res['data']), 2)
        
    def test_record_of_item(self):
        """
        api: /item/<int:item_id>/record
        methods: get: 获取一个条目下的所有记录
                 post: 在一个条目下创建一条记录
        """
        # 获取一个条目下的所有记录
        res = self.client.get(BASE_URL + '/item/1/record').get_json()
        self.assertEqual(res['status'], 200)
        self.assertEqual(len(res['data']), 2)

        # 在一个条目下创建一条记录，但未提供参数
        res = self.client.post(BASE_URL + '/item/1/record').get_json()
        self.assertEqual(res['status'], 400)

        # 在一个条目下创建一条记录，但条目不存在
        start = datetime(2019, 1, 12, 6, 0, 0)
        res = self.client.post(BASE_URL + '/item/100/record', data={'start': int(start.timestamp() * 1000)}).get_json()
        self.assertEqual(res['status'], 404)

        # 在一个条目下创建一条记录
        res = self.client.post(BASE_URL + '/item/1/record', data={'start': int(start.timestamp() * 1000)}).get_json()
        self.assertEqual(res['status'], 201)
        self.assertEqual(res['data']['start'], '2019-01-12T06:00:00')
        item = Item.query.get(1)
        self.assertEqual(len(item.records), 3)

    def test_record_with_time_filter(self):
        """测试 url 中带有 query string，即限定时间范围的情况"""
        from_time = int(datetime(2019, 1, 11, 0, 0, 0).timestamp() * 1000)
        to_time = int(datetime(2019, 1, 11, 12, 0, 0).timestamp() * 1000)
        qs = f'?from={from_time}&to={to_time}'
        res = self.client.get(BASE_URL + '/record'+qs).get_json()
        self.assertEqual(res['status'], 200)
        self.assertEqual(len(res['data']), 1)


class TagTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        category = Category(name='test_category')
        item = Item(name='test_item')
        item.category = category
        record_1 = Record(
            start=datetime(2019, 1, 10, 6, 0, 0),
            finish=datetime(2019, 1, 10, 7, 0, 0),
            remark='test_record_1'
        )
        record_2 = Record(
            start=datetime(2019, 1, 11, 6, 0, 0),
            finish=datetime(2019, 1, 11, 7, 0, 0),
            remark='test_record_2'
        )
        tag_1 = Tag(name='test_tag_1')
        tag_2 = Tag(name='test_tag_2')
        record_1.tags = [tag_1, tag_2]
        item.records = [record_1, record_2]
        db.session.add(item)
        db.session.commit()

    def test_tag(self):
        """
        api: /tag
        methods: get: 获取所有标签
        """
        # 获取所有标签
        res = self.client.get(BASE_URL + '/tag').get_json()
        self.assertEqual(res['status'], 200)
        self.assertEqual(len(res['data']), 2)

    def test_tag_member(self):
        """
        api: /tag/<int:tag_id>
        methods: get: 获取一个标签的详情
        """
        # 获取一个标签的详情
        res = self.client.get(BASE_URL + '/tag/1').get_json()
        self.assertEqual(res['status'], 200)
        self.assertEqual(res['data']['name'], 'test_tag_1')

        # 获取一个不存在（已删除）的标签的详情
        res = self.client.get(BASE_URL + '/tag/100').get_json()
        self.assertEqual(res['status'], 404)

    def test_tag_of_category(self):
        """
        api: /category/<int:category_id>/tag
        methods: get: 获取一个分类下的所有标签
        """
        # 获取一个分类下的所有标签
        res = self.client.get(BASE_URL + '/category/1/tag').get_json()
        self.assertEqual(res['status'], 200)
        self.assertEqual(len(res['data']), 2)

    def test_tag_of_item(self):
        """
        api: /item/<int:item_id>/tag
        methods: get: 获取一个条目下的所有标签
        """
        # 获取一个条目下的所有标签
        res = self.client.get(BASE_URL + '/item/1/tag').get_json()
        self.assertEqual(res['status'], 200)
        self.assertEqual(len(res['data']), 2)
        self.assertEqual(res['data'][0]['name'], 'test_tag_1')

    def test_tag_of_record(self):
        """
        api: /record/<int:record_id>/tag
        methods: post: 在一条记录下创建一个标签
                 delete: 在一条记录下删除一个标签
        """
        # 在一条记录下创建一个标签，但未提供参数
        res = self.client.post(BASE_URL + '/record/2/tag').get_json()
        self.assertEqual(res['status'], 400)

        # 在一条记录下创建一个标签，但记录不存在
        res = self.client.post(BASE_URL + '/record/100/tag', data={'name': 'test_tag_1'}).get_json()
        self.assertEqual(res['status'], 404)

        # 在一条记录下创建一个标签，此标签在其他记录中已使用
        res = self.client.post(BASE_URL + '/record/2/tag', data={'name': 'test_tag_1'}).get_json()
        self.assertEqual(res['status'], 201)
        self.assertEqual(res['data']['name'], 'test_tag_1')
        tag_1 = Tag.query.get(1)
        self.assertEqual(len(tag_1.records), 2)

        # 在一条记录下创建一个标签，此标签未其他记录中使用
        res = self.client.post(BASE_URL + '/record/2/tag', data={'name': 'test_tag_3'}).get_json()
        self.assertEqual(res['status'], 201)
        self.assertEqual(res['data']['name'], 'test_tag_3')
        tags = Tag.query.all()
        self.assertEqual(len(tags), 3)

        # 在一条记录下删除一个标签，但未提供参数
        res = self.client.delete(BASE_URL + '/record/2/tag').get_json()
        self.assertEqual(res['status'], 400)

        # 在一条记录下删除一个标签，但记录不存在
        res = self.client.delete(BASE_URL + '/record/100/tag', data={'id': 1}).get_json()
        self.assertEqual(res['status'], 404)

        # 在一条记录下删除一个标签，但标签不存在
        res = self.client.delete(BASE_URL + '/record/1/tag', data={'id': 100}).get_json()
        self.assertEqual(res['status'], 404)

        # 在一条记录下删除一个标签
        res = self.client.delete(BASE_URL + '/record/1/tag', data={'id': 1}).get_json()
        self.assertEqual(res['status'], 200)
        record = Record.query.get(1)
        self.assertEqual(len(record.tags), 1)


if __name__ == '__main__':
    unittest.main()
