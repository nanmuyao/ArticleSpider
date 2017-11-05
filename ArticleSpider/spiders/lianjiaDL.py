# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
import logging
import scrapy.settings

class LianjiadlSpider(scrapy.Spider):
    custom_settings = {
        'DOWNLOAD_DELAY': '0.25',
        'LOG_ENABLED' : True,
    }



    current_page_num = 2
    name = 'lianjiaDL'
    allowed_domains = ['dl.lianjia.com/']
    # start_urls = ['https://dl.lianjia.com/ershoufang/ganjingzi/']
    start_urls = ['https://dl.lianjia.com/ershoufang/rs大纺/']



    def parse(self, response):
        self.logger.info(self.settings.get('DOWNLOAD_DELAY'))
        # print("Existing settings: %s" % self.settings.attributes.keys())

        # post_nodes = response.css(".sellListContent .clear")
        # for post_node in post_nodes:
        #     house_title = post_node.css(".clear .title a::text").extract_first()
        #     totle_price = post_node.css(".totalPrice span::text").extract_first()
        #     houseInfo = post_node.css(".houseInfo::text").extract_first()
        #     unitPrice = post_node.css(".unitPrice span::text").extract_first()
        #     print("房子描述", house_title, "总价" + "万", "单价："+ unitPrice, "房子信息："+houseInfo)

        self.parase_detail(response)

        # 提取下一页并交给scrapy进行下载
        next_url = "https://dl.lianjia.com/ershoufang/ganjingzi/pg{}/".format(self.current_page_num)
        self.current_page_num = self.current_page_num + 1
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), dont_filter=True, callback=self.parse)

    def parase_detail(self, response):
        print("response.status=",response.status, "第{0}次请求".format(self.current_page_num))



        # post_nodes = response.css(".sellListContent .clear")
        # for post_node in post_nodes:
        #     house_title = post_node.css(".clear .title a::text").extract_first()
        #     totle_price = post_node.css(".totalPrice span::text").extract_first()
        #     houseInfo = post_node.css(".houseInfo::text").extract_first()
        #     unitPrice = post_node.css(".unitPrice span::text").extract_first()
        #     print("房子描述", house_title, "总价" + "万", "单价："+ unitPrice, "房子信息："+houseInfo)

