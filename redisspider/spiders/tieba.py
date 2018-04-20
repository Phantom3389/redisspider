# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
from redisspider.items import TiebaItem, TiebaLoader
from scrapy.http import Request
from urllib import parse


class TiebaSpider(RedisSpider):
    name = 'tieba'
    allowed_domains = ['tieba.baidu.com']
    start_urls = ['http://tieba.baidu.com/f?kw=%E6%B5%B7%E5%8D%97%E5%A4%A7%E5%AD%A6&ie=utf-8&pn=0']

    def parse(self, response):
        nodes = response.css(".j_thread_list.clearfix")
        for node in nodes:
            Loderitem = TiebaLoader(item=TiebaItem, response=node)
            Loderitem.add_css("url", ".j_th_tit a::attr(href)")
            Loderitem.add_css("title", ".j_th_tit a::attr(title)")
            tieba_item = Loderitem.load_item()
            yield tieba_item

        next_url = response.css(".next.pagination-item").extract_first()
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)
