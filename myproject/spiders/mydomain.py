# -*- coding: utf-8 -*-
import scrapy
import time
import re
import pymysql
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
from myproject import settings
from myproject.items import GoodsItem
from twisted.conch.insults.window import cursor


class MydomainSpider(CrawlSpider):
    name = 'mydomain'
    allowed_domains = ['http://www.meilele.com']
    #start_urls = ['http://www.meilele.com/category-chuangpintaojian']
    start_urls = ['http://www.meilele.com/jiaju']
    # 用来保持登录状态，可把chrome上拷贝下来的字符串形式cookie转化成字典形式，粘贴到此处
    cookies = {}
    
    # 发送给服务器的http头信息，有的网站需要伪装出浏览器头进行爬取，有的则不需要
    headers = {
        # 'Connection': 'keep - alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    }
    
    # 对请求的返回进行处理的配置
    meta = {
        'dont_redirect': True,  # 禁止网页重定向
        'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理
    }
#     def start_requests(self):
#         selectSQL = 'select * from mll_goods_data_1'
#         goods_ids_sql = self.cursor.execute(selectSQL)
#         goods_ids = self.cursor.fetchall()
#         for row in goods_ids:
#             url = 'http://www.meilele.com/category-chuangpintaojian/goods-%s.html?page=1&index=1' % row[1]
#             yield scrapy.Request(url)
#     def __init__(self):
#         self.connect = pymysql.connect(
#             host=settings.MYSQL_HOST,
#             db=settings.MYSQL_DBNAME,    
#             user=settings.MYSQL_USER,
#             passwd=settings.MYSQL_PASSWD,
#             charset='utf8',
#             use_unicode=True)
#         self.cursor = self.connect.cursor()
#     def parse(self, response):
#         #详情数据提取
#         item = GoodsItem()
#         item['goods_title'] = ''.join(response.xpath('//*[@id="JS_goods_info_panel"]/div[1]/h4[1]/text()').extract())
#         item['goods_desc'] = ''.join(response.xpath('//*[@id="JS_goods_sub_title"]/text()').extract())
#         item['goods_type'] = 0
#         item['goods_sn'] = ''.join(response.xpath('//*[@id="JS_goods_info_panel"]/div/h4/span/text()').extract()).replace("编号：", "")
#         item['goods_id'] = "".join(response.xpath('//div[@id="static_dynamic"]/@goods_id').extract()).encode("GBK", "ignore")
#         item['goods_price'] = "".join(response.xpath('//*[@id="JS_effect_price"]/text()').extract()).encode("GBK", "ignore")
#         item['add_time'] = time.time()
#         yield item
    def parse(self, response):
        #获取栏目页的列表页链接
        #cat_url = response.xpath('//*[@id="JS_fixed_goods_cat"]/div[@class="in"]/div[@class="body"]/div/dl/dd/a/@href').extract()
        cat_url = response.xpath('//*[@id="JS_mll_menu_map"]/li/dl/dd/a/@href').extract()
        for i in cat_url:
            new_url = "http://www.meilele.com" + i
            yield scrapy.Request(new_url, callback=self.parse_list, dont_filter=True)
    def parse_list(self, response):
        #获取列表页最大分页数
        arr = []
        list_num = response.xpath('//*[@class="page-panel"]/div/div[@class="p-list"]/a[@class="p-item p-num"]/text()').extract()
        for num in list_num:
            arr.append(int(num))
        if len(arr):
            max_num = max(arr)
        else:
            max_num = 1
        #获取列表页的分页链接
        #将分页链接处理
        list_url = "".join(response.xpath('//*[@class="page-panel"]/div/div[@class="p-list"]/span[@class="p-item p-cur"]/@href').extract()).encode("GBK", "ignore")
        new_arr = list_url.split("/")
        for everyPage in range(1, int(max_num)+1):
            new_url = "http://www.meilele.com/" + new_arr[1] +"/list-p" + str(everyPage) + "/" + new_arr[2]
            yield scrapy.Request(new_url, callback=self.parse_goods_link, dont_filter=True)
    def parse_goods_link(self, response):
        #获取列表页的详情页链接
        url = response.xpath('//*[@id="JS_list_panel"]/div/ul/li/div[@class="g-dtl"]/a[@class="d-name"]/@href').extract()
        for i in url:
            new_url = "http://www.meilele.com" + i
            yield scrapy.Request(new_url, callback=self.parse_detail, dont_filter=True)
    def parse_detail(self, response):
        #详情数据提取
        item = GoodsItem()
        item['goods_title'] = ''.join(response.xpath('//*[@id="JS_goods_info_panel"]/div[1]/h4[1]/text()').extract())
        item['goods_desc'] = ''.join(response.xpath('//*[@id="JS_goods_sub_title"]/text()').extract())
        item['goods_type'] = 0
        item['goods_sn'] = ''.join(response.xpath('//*[@id="JS_goods_info_panel"]/div/h4/span/text()').extract()).replace("编号：", "")
        item['goods_id'] = "".join(response.xpath('//div[@id="static_dynamic"]/@goods_id').extract()).encode("GBK", "ignore")
        item['goods_price'] = "".join(response.xpath('//*[@id="JS_effect_price"]/text()').extract()).encode("GBK", "ignore")
        item['add_time'] = time.time()
        yield item