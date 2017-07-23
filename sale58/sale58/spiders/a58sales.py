# -*- coding: utf-8 -*-

import scrapy
from scrapy_redis.spiders import RedisSpider
from sale58.items import Inof58Item, Inof58Loader
from redis import Redis
from scrapy import log
from time import sleep


class A58salesSpider(RedisSpider):
    name = "58sales"
    redis_key = 'A58salesSpider:58_urls'
    # allowed_domains = ["58.com"]
    # start_urls = (
    #     'http://bj.58.com/pbdn/0/',
    # )

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domans = filter(None, domain.split(','))
        super(A58salesSpider, self).__init__(*args, **kwargs)
        self.url = 'http://bj.58.com'


    def parse(self, response):
        info = Inof58Loader(response=response)
        PageUrl = response.xpath('//a[@class="next"]/@href').extract()
        self.log(PageUrl, level=log.DEBUG)
        r = Redis()
        if PageUrl != []:
            r.lpush('A58salesSpider:58_urls', self.url + PageUrl[0])
            sleep(1)
            info.add_value('UrlofPage', self.url + PageUrl[0])
        urls = response.xpath(".//table[@class='tbimg']/tbody/tr/td[@class='t']/a/@href").extract()
        if urls:
            for url in urls:
                print url
                r.lpush('A58salesRedis:start_urls', url)
        yield info.load_item()