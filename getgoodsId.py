# -*- coding: utf-8 -*-
import scrapy
import time
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
from myproject import settings
from myproject.items import GoodsItem1


class getgoodsIdSpider(CrawlSpider):
    return
    name = 'getgoodsId'
    allowed_domains = ['http://www.meilele.com']
    start_urls = []
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
    
    def start_requests(self):
        for everyPage in range(1, 63):
            #url = 'http://www.meilele.com/category-dengshizhaoming/list-p%s/?from=page#p' % everyPage
            #url = 'http://www.meilele.com/category-wofang/list-p%s/?from=page#p' % everyPage
            url = 'http://www.meilele.com/category-chuangshangyongpin/list-p%s/?from=page#p' % everyPage
            yield Request(url,callback=self.parse, headers=self.headers,cookies=self.cookies, meta=self.meta)
    def parse(self, response):
        item = GoodsItem1()
        goods_ids = response.xpath('//div[@id="JS_list_panel"]/div/ul/li/@data-goods-id').extract()
        for goods_id in goods_ids:
            item['goods_id'] = goods_id
            item['add_time'] = time.time()
            yield item