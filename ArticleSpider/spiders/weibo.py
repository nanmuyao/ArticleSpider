# -*- coding: utf-8 -*-
import scrapy


class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['www.weibo.com']
    start_urls = ['http://www.weibo.com/']

    def parse(self, response):
        pass
