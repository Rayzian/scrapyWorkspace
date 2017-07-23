from scrapy_redis.spiders import RedisSpider
from sale58.items import Inof58Loader, Inof58Item
# from scrapy import log


class A58salesRedis(RedisSpider):
    '''spider that reads urls from redis queue (myspider:start_urls).'''
    name = '58sales_redis'
    redis_key = 'A58salesRedis:start_urls'

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domans = filter(None, domain.split(','))
        super(A58salesRedis, self).__init__(*args, **kwargs)


    def parse(self, response):

        title = response.xpath('//h1/text()').extract()
        if title:
            title = title[0]
        else:
            title = None
        price = response.xpath('//span[@class="price c_f50"]/text()').extract()
        if price:
            price = price[0]
        else:
            price = response.xpath('//span[@class="price_now"]/i/text()').extract()
            if price:
                price = price[0]
            else:
                price = None
        quality = response.xpath('//ul[@class="suUl"]/li/div[@class="su_con"]/text()').extract()
        if quality:
            quality = quality[0]
        else:
            quality = None
        area = response.xpath('//span[@class="c_25d"]/a/text()'.strip())
        if area == []:
            area = 'None'
        elif len(area) == 1:
            area = area[0].extract()
        else:
            area = area[0].extract() + '-' + area[1].extract()
        item = Inof58Item(title=title, price=price, quality=quality, area=area)
        yield item





