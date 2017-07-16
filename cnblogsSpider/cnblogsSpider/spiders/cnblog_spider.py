# coding:utf-8

import scrapy
from scrapy import Selector
from cnblogsSpider.items import CnblogsspiderItem

class CnBlogsSpider(scrapy.Spider):
    name = "blogSpider"
    allowed_domains = ["cnblogs.com"]
    start_urls = [
        "http://www.cnblogs.com/qiyeboy/default.html?page=1"
    ]


    def parse(self, response):
        for paper in (response.xpath(".//*[@class='day']")):
            url = paper.xpath(".//*[@class='postTitle']/a/@href").extract()[0]
            title = paper.xpath(".//*[@class='postTitle']/a/text()").extract()[0]
            time = paper.xpath(".//*[@class='dayTitle']/a/text()").extract()[0]
            content = paper.xpath(".//*[@class='postTitle']/a/text()").extract()[0]
            item = CnblogsspiderItem(url=url, title=title, date=time, content=content)
            yield item
        next_page = Selector(response).re(u'<a href="(\S*)">下一页</a>')
        if next_page:
            yield scrapy.Request(url=next_page[0], callback=self.parse)

    def parser_body(self, response):
        item = response.meta["item"]
        body = response.xpath(".//*[@class='postBody']")
        item["cimage_urls"] = body.xpath(".//img//@src").etract()
        yield item
