# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
from sohu.utility import get_time
import scrapy
import pymysql
import os




class SohuPipeline(object):
    def process_item(self, item, spider):
        return item

class SohuImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        image_guid = request.url.split('/')[-1]
        return "full/{a}/{b}".format(a = get_time(), b= image_guid)

    def get_media_requests(self, item, info):
        if( len(item['img_url']) > 0):
            for img in item['img_url']:
                if img.startswith('//') :
                    yield scrapy.Request('http://' + img, meta={"item": item})
                elif img.startswith('http') :
                    yield scrapy.Request(img, meta={"item": item})
        else:
            return


    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['img_path'] = image_paths
        return item


class SohuStoreToMySqlPipeline(object):
    def __init__(self):
        self.connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='news',
                                          charset='utf8')
    def process_item(self, item, spider):
        with self.connection.cursor() as self.cursor:
            sql = 'INSERT INTO oii_spy_news (title, update_time, thumb, copy_from, content' \
                  ') VALUES (%s, %s, %s, %s, %s)'
                  
            self.cursor.execute(sql, (item['title'][0].strip(), item['updatetime'][0][:-3].strip(),
                                      item['img_path'][0].strip(), item['copy_from'][0].strip(),
                                      item['content'][0].strip()))
            self.connection.commit()

    def spider_closed(self, spider):
        self.cursor.close()
        self.connection.close();