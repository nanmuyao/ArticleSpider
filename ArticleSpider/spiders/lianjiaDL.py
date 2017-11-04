# -*- coding: utf-8 -*-
import scrapy


class LianjiadlSpider(scrapy.Spider):
    name = 'lianjiaDL'
    allowed_domains = ['https://dl.lianjia.com/']
    # start_urls = ['https://dl.lianjia.com/ershoufang/ganjingzi/']
    start_urls = ['https://dl.lianjia.com/ershoufang/rs大纺/']




    def parse(self, response):

        post_nodes = response.css(".sellListContent .clear")
        for post_node in post_nodes:
            house_title = post_node.css(".clear .title a::text").extract_first()
            totle_price = post_node.css(".totalPrice span::text").extract_first()
            houseInfo = post_node.css(".houseInfo::text").extract_first()
            unitPrice = post_node.css(".unitPrice span::text").extract_first()
            print("房子描述", house_title, "总价" + "万", "单价："+ unitPrice, "房子信息："+houseInfo)

    def parase_detail(self):
        pass
