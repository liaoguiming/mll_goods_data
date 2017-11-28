# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import scrapy

from myproject import settings
from myproject.items import GoodsItem,GoodsItem1

class MyprojectPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        if item.__class__ == GoodsItem:
            if item['goods_id'] == 0 or item['goods_id'] == '' or item['goods_sn'] == '':
                return
            self.cursor.execute("""select * from mll_goods_data where goods_id = %s""", item['goods_id'])
            ret = self.cursor.fetchone()
            if ret:
                self.cursor.execute(
                    """update mll_goods_data set goods_title = %s,goods_desc = %s,goods_type = %s,
                        add_time = %s,goods_price = %s,goods_id = %s,goods_sn = %s where goods_id = %s""",
                    (item['goods_title'],
                     item['goods_desc'],
                     item['goods_type'],
                     item['add_time'],
                     item['goods_price'],
                     item['goods_id'],
                     item['goods_sn'],
                     item['goods_id']))
            else:
                self.cursor.execute(
                    """insert into mll_goods_data(goods_id,goods_title,goods_desc,goods_type,add_time,goods_price,goods_sn)
                      value (%s,%s,%s,%s,%s,%s,%s)""",
                    (item['goods_id'],
                     item['goods_title'],
                     item['goods_desc'],
                     item['goods_type'],
                     item['add_time'],
                     item['goods_price'],
                     item['goods_sn']))
            self.connect.commit()
            return item
        elif item.__class__ == GoodsItem1:
            if item['goods_id'] == 0 or item['goods_id'] == '':
                return
            self.cursor.execute("""select * from mll_goods_data where goods_id = %s""", item['goods_id'])
            ret = self.cursor.fetchone()
            if ret:
                print 1
            else:
                self.cursor.execute(
                    """insert into mll_goods_data_1(goods_id,add_time)
                      value (%s,%s)""",
                    (item['goods_id'],
                     item['add_time']))
            self.connect.commit()
            return item
