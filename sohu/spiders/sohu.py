import scrapy
import re
import os
from sohu.items import SohuItem
from sohu.utility import get_time


class sohu(scrapy.Spider):
    name = 'sohu'
    allowed_domains = ['www.sohu.com']
    start_urls = ['http://www.sohu.com']

    def parse(self, response):
        for sel in response.xpath('//div[@class = "focus-news-box"]/div/div[@class = "list16"][1]/ul/li'):
            item = SohuItem()
            item['title'] = sel.xpath('.//a/@title').extract()
            item['href'] = sel.xpath('.//a/@href').extract()
            #yield item
            yield scrapy.Request(response.urljoin(item['href'][0]), meta={'item': item}, callback=self.parse_content)

    def parse_content(self, response):
        item = response.meta['item']
        item['updatetime'] = response.xpath('//span[ @id ="news-time" ]/@data-val').extract()
        item['img_url'] = response.css('#mp-editor img::attr(src)').extract()
        item['copy_from'] = response.xpath('//div[ @id = "user-info"]/h4/a/text()').extract()
        item = self.get_content(item, response)
        yield item

    def get_content(self, item, response):
        content = response.xpath('//article[ @id = "mp-editor"]').extract()
        reg = r'src="(.*?[\.jpg|\.png|\.jpeg|\.bmp|\.gif])"'

        pattern = re.compile(reg)
        re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)
        content[0] = re_script.sub('', content[0])
        regA = r'<a .* id="backsohucom" .*</a>'
        content[0] = re.sub(regA, "", content[0])
        imgArr = pattern.findall( str(content))

        if len(imgArr) > 0:
            for i in imgArr:
                content[0] = content[0].replace(i, "/news/sohu/sohu/images/full/{a}/{b}".format(a = get_time(), b=os.path.basename(i)))
        item['content'] = content
        return item
