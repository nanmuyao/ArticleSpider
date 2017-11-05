# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
import logging
import scrapy.settings
from ArticleSpider.items import LianJiaItem, ArticleItemLoader

class LianjiadlSpider(scrapy.Spider):
    custom_settings = {
        'DOWNLOAD_DELAY': '5',
        'LOG_ENABLED' : True,
        'ITEM_PIPELINES' : {'ArticleSpider.pipelines.CSVPipeline':5},
    }

    current_page_num = 2
    name = 'lianjiaDL'
    allowed_domains = ['dl.lianjia.com/']
    # start_urls = ['https://dl.lianjia.com/ershoufang/ganjingzi/']
    start_urls = ['https://dl.lianjia.com/ershoufang/rs大纺/']

    def parse(self, response):
        # self.logger.info(self.settings.get('DOWNLOAD_DELAY'))
        # print("Existing settings: %s" % self.settings.attributes.keys())

        # post_nodes = response.css(".sellListContent .clear")
        # for post_node in post_nodes:
        #     house_title = post_node.css(".clear .title a::text").extract_first()
        #     totle_price = post_node.css(".totalPrice span::text").extract_first()
        #     houseInfo = post_node.css(".houseInfo::text").extract_first()
        #     unitPrice = post_node.css(".unitPrice span::text").extract_first()
        #     print("房子描述", house_title, "总价" + "万", "单价："+ unitPrice, "房子信息："+houseInfo)

        post_nodes = response.css(".sellListContent .clear")
        for post_node in post_nodes:
            lianjia_item = LianJiaItem()
            item_loader = ArticleItemLoader(item=LianJiaItem(), response=response)
            house_title = post_node.css(".clear .title a::text").extract_first()
            unitPrice = post_node.css(".unitPrice span::text").extract_first()
            item_loader.add_value("house_title", house_title)
            item_loader.add_value('house_unit_price', unitPrice)

            lianjia_item = item_loader.load_item()

            yield lianjia_item

        # 提取下一页并交给scrapy进行下载
        next_url = "https://dl.lianjia.com/ershoufang/ganjingzi/pg{}/".format(self.current_page_num)
        self.current_page_num = self.current_page_num + 1
        if (self.current_page_num > 3) :
            self.close_spider()
            return
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), dont_filter=True, callback=self.parse)

    def parase_detail(self, response):
        pass
