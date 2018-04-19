# _*_ encoding: utf-8 _*_
__author__ = 'Phantom3389'
__date__ = '2018/3/12 15:13'

# -*- coding: utf-8 -*-
from scrapy.http import Request
from urllib import parse
from scrapy_redis.spiders import RedisSpider
from redisspider.items import JobBoleItem, ArticleItemLoader


class JobboleSpider(RedisSpider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        post_nodes = response.css("#archive div.floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": parse.urljoin(response.url, image_url)}, callback=self.detail_parse)

        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def detail_parse(self, response):
        #通过item loader加载item
        front_image_url = response.meta.get("front_image_url", "")
        item_loader = ArticleItemLoader(item=JobBoleItem(), response=response)
        item_loader.add_css("title", ".entry-header h1::text")
        item_loader.add_value("url", response.url)
        item_loader.add_css("create_date", "p.entry-meta-hide-on-mobile::text")
        item_loader.add_css("praise_nums", "span.vote-post-up h10::text")
        item_loader.add_css("fav_nums", "span.bookmark-btn::text")
        item_loader.add_css("comment_nums", "a[href='#article-comment'] span::text")
        item_loader.add_css("content", "div.entry")
        item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")
        item_loader.add_value("front_image_url", [front_image_url])

        article_item = item_loader.load_item()

        yield article_item
