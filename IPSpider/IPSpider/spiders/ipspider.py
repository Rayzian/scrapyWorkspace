# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy import Selector
from IPSpider.items import IpspiderItem


class IpspiderSpider(scrapy.Spider):
    name = "ipspider"
    allowed_domains = ["goubanjia.com"]
    start_urls = (
        'http://www.goubanjia.com/free/index1.shtml',
    )

    def parse(self, response):
        try:
            for div in (response.xpath("//div[@id='list']/table[@class='table']/tbody/tr/td[@class='ip']")):
                tag_str = re.findall(r'>(\S+)</|>\W+<', str(div.extract()))
                if tag_str:
                    ip_port = ""
                    for temp_str in tag_str:
                        if not temp_str:
                            temp_str = temp_str.replace("", ":")
                        target_str = re.search(r'[^<>/]\d+|\d+\.|\.|\d+|\:', temp_str)

                        if target_str:
                            ip_port += target_str.group()
                    print ip_port
                    str_list = ip_port.strip().split(":")
                    ip = str_list[0]
                    port = str_list[1]

                    item = IpspiderItem(ip=ip, port=port)
                    yield item

            current_page = response.xpath(".//span[@class='current']/text()")
            if current_page:
                current_page = current_page.extract()[0]

            nextPage_list = Selector(response=response).re(u'<a href="(\S*)">\d+</a>')
            index = ""
            if nextPage_list:
                for temp in nextPage_list:
                    page_num = re.search(r'\d+', str(temp))
                    if page_num:
                        if int(page_num.group()) > int(current_page):
                            index = nextPage_list.index(temp)
                            break

            next_page = nextPage_list[int(index)]
            print next_page

            yield scrapy.Request(url="http://www.goubanjia.com/free/" + str(next_page), callback=self.parse)

        except Exception, e:
            print e
            pass
