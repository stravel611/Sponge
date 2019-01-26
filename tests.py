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
        self.runner = app.test_cli_runner()

        db.create_all()

    def tearDown(self):
        db.drop_all()
        self.context.pop()


class CliCommandTestCase(BaseTestCase):
    def test_initdb(self):
        result = self.runner.invoke(args=['init-db'])
        self.assertIn('数据库初始化完毕！', result.output)

    def test_forge(self):
        result = self.runner.invoke(args=['forge', '--drop'], input='y\n')
        self.assertIn('数据生成完毕！', result.output)
        categories = Category.query.all()
        self.assertEqual(5, len(categories))
        items = Item.query.all()
        self.assertEqual(20, len(items))
        records = Record.query.all()
        self.assertEqual(50, len(records))
        tags = Tag.query.all()
        self.assertEqual(10, len(tags))


class CategoryTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        category = Category(name='test_category')
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
        self.assertEqual(200, res['status'])
        self.assertEqual('test_category', res['data'][0]['name'])

        # 创建一个分类，但未提供参数
        res = self.client.post(BASE_URL + '/category').get_json()
        self.assertEqual(400, res['status'])

        # 创建一个分类，但分类已存在
        res = self.client.post(BASE_URL + '/category', data={'name': 'test_category'}).get_json()
        self.assertEqual(409, res['status'])

        # 创建一个分类
        res = self.client.post(BASE_URL + '/category', data={'name': 'new_category'}).get_json()
        self.assertEqual(201, res['status'])
        self.assertEqual('new_category', res['data']['name'])
        self.assertEqual(2, len(Category.query.all()))

    def test_category_member(self):
        """
        api: /category/<int:category_id>
        methods: get: 获取一个分类的详情
                 put: 更新一个分类的信息
                 delete: 删除一个分类
        """
        # 更新一个不存在的分类
        res = self.client.put(BASE_URL + '/category/100').get_json()
        self.assertEqual(404, res['status'])

        # 更新一个分类，但未提供参数
        res = self.client.put(BASE_URL + '/category/1').get_json()
        self.assertEqual(400, res['status'])

        # 更新一个分类的名称，但与原内容相同
        res = self.client.put(BASE_URL + '/category/1', data={'name': 'test_category'}).get_json()
        self.assertEqual(409, res['status'])

        # 更新一个分类的名称
        res = self.client.put(BASE_URL + '/category/1', data={'name': 'changed_name'}).get_json()
        self.assertEqual(200, res['status'])
        self.assertEqual('changed_name', res['data']['name'])
        category = Category.query.get(1)
        self.assertEqual('changed_name', category.name)

        # 获取一个分类
        res = self.client.get(BASE_URL + '/category/1').get_json()
        self.assertEqual(200, res['status'])
        self.assertEqual('changed_name', res['data']['name'])

        # 删除一个不存在的分类
        res = self.client.delete(BASE_URL + '/category/100').get_json()
        self.assertEqual(404, res['status'])

        # 删除一个分类
        res = self.client.delete(BASE_URL + '/category/1').get_json()
        self.assertEqual(200, res['status'])
        category = Category.query.get(1)
        self.assertIsNone(category)

        # 获取一个不存在（已删除）的分类
        res = self.client.get(BASE_URL + '/category/1').get_json()
        self.assertEqual(404, res['status'])

    def test_calculation_of_category(self):
        """
        api: /category/<int:category_id>/calculation
        methods: get: 获取一个分类下的所有条目的记录的时间总和（秒）
        """
        category = Category.query.first()
        item = Item(name='test_item')
        record = Record(
            start=datetime(2019, 1, 10, 6, 0, 0),
            finish=datetime(2019, 1, 10, 7, 0, 0)
        )
        item.category = category
        record.item = item
        db.session.add(record)
        db.session.commit()
        res = self.client.get(BASE_URL + '/category/1/calculation').get_json()
        self.assertEqual(200, res['status'])
        self.assertEqual(3600, res['data'][0]['value'])


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
        self.assertEqual(200, res['status'])
        self.assertEqual('test_item', res['data'][0]['name'])

        # 创建一个条目，但未提供参数
        res = self.client.post(BASE_URL + '/item').get_json()
        self.assertEqual(400, res['status'])

        # 创建一个条目，但条目已存在
        res = self.client.post(BASE_URL + '/item', data={'name': 'test_item'}).get_json()
        self.assertEqual(409, res['status'])

        # 创建一个条目
        res = self.client.post(BASE_URL + '/item', data={'name': 'new_item'}).get_json()
        self.assertEqual(201, res['status'])
        self.assertEqual('new_item', res['data']['name'])
        self.assertEqual(2, len(Item.query.all()))

    def test_item_member(self):
        """
        api: /item/<int:item_id>
        methods: get: 获取一个条目的详情
                 put: 更新一个条目的信息
                 delete: 删除一个条目
        """
        # 更新一个不存在的条目
        res = self.client.put(BASE_URL + '/item/100').get_json()
        self.assertEqual(404, res['status'])

        # 更新一个条目，但未提供参数
        res = self.client.put(BASE_URL + '/item/1').get_json()
        self.assertEqual(400, res['status'])

        # 更新一个条目的名称，但与原内容相同
        res = self.client.put(BASE_URL + '/item/1', data={'name': 'test_item'}).get_json()
        self.assertEqual(409, res['status'])

        # 更新一个条目的名称
        res = self.client.put(BASE_URL + '/item/1', data={'name': 'changed_name'}).get_json()
        self.assertEqual(200, res['status'])
        self.assertEqual('changed_name', res['data']['name'])
        item = Item.query.get(1)
        self.assertEqual('changed_name', item.name)

        # 获取一个条目
        res = self.client.get(BASE_URL + '/item/1').get_json()
        self.assertEqual(200, res['status'])
        self.assertEqual('changed_name', res['data']['name'])

        # 删除一个不存在的条目
        res = self.client.delete(BASE_URL + '/item/100').get_json()
        self.assertEqual(404, res['status'])

        # 删除一个条目
        res = self.client.delete(BASE_URL + '/item/1').get_json()
        self.assertEqual(200, res['status'])
        item = Item.query.get(1)
        self.assertIsNone(item)

        # 获取一个不存在（已删除）的条目
        res = self.client.get(BASE_URL + '/item/1').get_json()
        self.assertEqual(404, res['status'])

    def test_item_of_category(self):
        """
        api: /category/<int:category_id>/item
        methods: get: 获取一个分类下的所有条目
                 post: 在一个分类下创建一个条目
        """
        # 获取一个分类下的所有条目
        res = self.client.get(BASE_URL + '/category/1/item').get_json()
        self.assertEqual(200, res['status'])
        self.assertEqual('test_item', res['data'][0]['name'])

        # 在一个分类下创建一个条目，但未提供参数
        res = self.client.post(BASE_URL + '/category/1/item').get_json()
        self.assertEqual(400, res['status'])

        # 在一个分类下创建一个条目，但条目已存在
        res = self.client.post(BASE_URL + '/category/1/item', data={'name': 'test_item'}).get_json()
        self.assertEqual(409, res['status'])

        # 在一个分类下创建一个条目
        res = self.client.post(BASE_URL + '/category/1/item', data={'name': 'new_item'}).get_json()
        self.assertEqual(201, res['status'])
        self.assertEqual('new_item', res['data']['name'])
        category = Category.query.get(1)
        self.assertEqual(len(category.items), 2)

    def test_calculation_of_item(self):
        """
        api: /category/<int:category_id>/calculation
        methods: get: 获取一个分类下的所有条目的记录的时间总和（秒）
        """
        item = Item.query.first()
        record = Record(
            start=datetime(2019, 1, 10, 6, 0, 0),
            finish=datetime(2019, 1, 10, 7, 0, 0)
        )
        record.item = item
        db.session.add(record)
        db.session.commit()
        res = self.client.get(BASE_URL + '/category/1/calculation').get_json()
        self.assertEqual(200, res['status'])
        self.assertEqual(3600, res['data'][0]['value'])


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
        methods: get: 获取所有记录，按开始时间降序排序
        """
        # 获取所有记录
        res = self.client.get(BASE_URL + '/record').get_json()
        self.assertEqual(200, res['status'])
        self.assertEqual('test_record_2', res['data'][0]['remark'])

    def test_record_member(self):
        """
        api: /record/<int:record_id>
        methods: get: 获取一条记录的详情
                 put: 更新一条记录的信息
                 delete: 删除一条记录
        """
        # 更新一条不存在的记录
        res = self.client.put(BASE_URL + '/record/100').get_json()
        self.assertEqual(404, res['status'])

        # 更新一条记录，但未提供参数
        res = self.client.put(BASE_URL + '/record/1').get_json()
        self.assertEqual(400, res['status'])

        # 更新一条记录的结束时间
        new_finish = datetime(2019, 1, 10, 8, 0, 0)
        res = self.client.put(BASE_URL + '/record/1', data={'finish': int(new_finish.timestamp() * 1000)}).get_json()
        self.assertEqual(200, res['status'])
        self.assertEqual('1月10日 08:00:00', res['data']['finish'])
        record = Record.query.get(1)
        self.assertEqual(new_finish, record.finish)

        # 更新一条记录的备注，但与原内容相同
        res = self.client.put(BASE_URL + '/record/1', data={'remark': 'test_record_1'}).get_json()
        self.assertEqual(409, res['status'])

        # 更新一条记录的备注
        res = self.client.put(BASE_URL + '/record/1', data={'remark': 'changed_remark'}).get_json()
        self.assertEqual(200, res['status'])
        self.assertEqual('changed_remark', res['data']['remark'])
        record = Record.query.get(1)
        self.assertEqual('changed_remark', record.remark)

        # 获取一条记录
        res = self.client.get(BASE_URL + '/record/1').get_json()
        self.assertEqual(200, res['status'])
        self.assertEqual('changed_remark', res['data']['remark'])

        # 删除一条不存在的记录
        res = self.client.delete(BASE_URL + '/record/100').get_json()
        self.assertEqual(404, res['status'])

        # 删除一条记录
        res = self.client.delete(BASE_URL + '/record/1').get_json()
        self.assertEqual(200, res['status'])
        record = Record.query.get(1)
        self.assertIsNone(record)

        # 获取一条不存在（已删除）的记录
        res = self.client.get(BASE_URL + '/record/1').get_json()
        self.assertEqual(404, res['status'])

    def test_record_of_category(self):
        """
        api: /category/<int:category_id>/record
        methods: get: 获取一个分类下的所有记录，按开始时间降序排序
        """
        # 获取一个分类下的所有记录
        res = self.client.get(BASE_URL + '/category/1/record').get_json()
        self.assertEqual(200, res['status'])
        self.assertEqual(2, len(res['data']))

    def test_record_of_item(self):
        """
        api: /item/<int:item_id>/record
        methods: get: 获取一个条目下的所有记录，按开始时间降序排序
                 post: 在一个条目下创建一条记录
        """
        # 获取一个条目下的所有记录
        res = self.client.get(BASE_URL + '/item/1/record').get_json()
        self.assertEqual(200, res['status'])
        self.assertEqual(2, len(res['data']))

        # 在一个条目下创建一条记录，但条目不存在
        res = self.client.post(BASE_URL + '/item/100/record').get_json()
        self.assertEqual(404, res['status'])

        # 在一个条目下创建一条记录
        res = self.client.post(BASE_URL + '/item/1/record').get_json()
        self.assertEqual(201, res['status'])
        self.assertIsNotNone(res['data']['start'])
        item = Item.query.get(1)
        self.assertEqual(3, len(item.records))
        
    def test_record_proceeding(self):
        """
        api: /record/proceeding
        methods: get: 获取正在进行的记录
        """
        # 获取正在进行的记录
        res = self.client.get(BASE_URL + '/record/proceeding').get_json()
        self.assertEqual(200, res['status'])
        self.assertIsNone(res['data']['start'])
        
        # 添加一条未完成记录，并获取该记录
        unfinished_record = Record(start=datetime(2019, 1, 12, 10, 0, 0))
        db.session.add(unfinished_record)
        db.session.commit()
        res = self.client.get(BASE_URL + '/record/proceeding').get_json()
        self.assertEqual(200, res['status'])
        self.assertIsNotNone(res['data']['start'])
        

    def test_record_with_time_filter(self):
        """测试 url 中带有 query string，即限定时间范围的情况"""
        from_time = int(datetime(2019, 1, 11, 0, 0, 0).timestamp() * 1000)
        to_time = int(datetime(2019, 1, 11, 12, 0, 0).timestamp() * 1000)
        qs = f'?from={from_time}&to={to_time}'
        res = self.client.get(BASE_URL + '/record' + qs).get_json()
        self.assertEqual(200, res['status'])
        self.assertEqual(1, len(res['data']))


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
        self.assertEqual(200, res['status'])
        self.assertEqual(2, len(res['data']))

    def test_tag_member(self):
        """
        api: /tag/<int:tag_id>
        methods: get: 获取一个标签的详情
        """
        # 获取一个标签的详情
        res = self.client.get(BASE_URL + '/tag/1').get_json()
        self.assertEqual(200, res['status'])
        self.assertEqual('test_tag_1', res['data']['name'])

        # 获取一个不存在（已删除）的标签的详情
        res = self.client.get(BASE_URL + '/tag/100').get_json()
        self.assertEqual(404, res['status'])

    def test_tag_of_category(self):
        """
        api: /category/<int:category_id>/tag
        methods: get: 获取一个分类下的所有标签
        """
        # 获取一个分类下的所有标签
        res = self.client.get(BASE_URL + '/category/1/tag').get_json()
        self.assertEqual(200, res['status'])
        self.assertEqual(2, len(res['data']))

    def test_tag_of_item(self):
        """
        api: /item/<int:item_id>/tag
        methods: get: 获取一个条目下的所有标签
        """
        # 获取一个条目下的所有标签
        res = self.client.get(BASE_URL + '/item/1/tag').get_json()
        self.assertEqual(200, res['status'])
        self.assertEqual(2, len(res['data']))

    def test_tag_of_record(self):
        """
        api: /record/<int:record_id>/tag
        methods: post: 在一条记录下创建一个标签
                 delete: 在一条记录下删除一个标签
        """
        # 在一条记录下创建一个标签，但未提供参数
        res = self.client.post(BASE_URL + '/record/2/tag').get_json()
        self.assertEqual(400, res['status'])

        # 在一条记录下创建一个标签，但记录不存在
        res = self.client.post(BASE_URL + '/record/100/tag', data={'name': 'test_tag_1'}).get_json()
        self.assertEqual(404, res['status'])

        # 在一条记录下创建一个标签，此标签在其他记录中已使用
        res = self.client.post(BASE_URL + '/record/2/tag', data={'name': 'test_tag_1'}).get_json()
        self.assertEqual(201, res['status'])
        self.assertEqual('test_tag_1', res['data']['name'])
        tag_1 = Tag.query.get(1)
        self.assertEqual(2, len(tag_1.records))

        # 在一条记录下创建一个标签，此标签未其他记录中使用
        res = self.client.post(BASE_URL + '/record/2/tag', data={'name': 'test_tag_3'}).get_json()
        self.assertEqual(201, res['status'])
        self.assertEqual('test_tag_3', res['data']['name'])
        tags = Tag.query.all()
        self.assertEqual(3, len(tags))

        # 在一条记录下删除一个标签，但未提供参数
        res = self.client.delete(BASE_URL + '/record/2/tag').get_json()
        self.assertEqual(400, res['status'])

        # 在一条记录下删除一个标签，但记录不存在
        res = self.client.delete(BASE_URL + '/record/100/tag?id=1', data={'id': 1}).get_json()
        self.assertEqual(404, res['status'])

        # 在一条记录下删除一个标签，但标签不存在
        res = self.client.delete(BASE_URL + '/record/1/tag?id=100').get_json()
        self.assertEqual(404, res['status'])

        # 在一条记录下删除一个标签
        res = self.client.delete(BASE_URL + '/record/1/tag?id=1').get_json()
        self.assertEqual(200, res['status'])
        record = Record.query.get(1)
        self.assertEqual(1, len(record.tags))


if __name__ == '__main__':
    unittest.main()
