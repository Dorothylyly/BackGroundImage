# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

from backgroundImages.settings import IMAGES_STORE
import redis
import os®
from backgroundImages import test




class ImagePipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None):
        url = request.url
        file_name = IMAGES_STORE+"/"+request.meta['item']['folder_name']+"/"+url.split("/")[-1]
        return file_name

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Image Downloaded Failed')
        return item

    def get_media_requests(self, item, info):
        self.picture_dir = item['folder_name']
        item['url'] = str(item['url']).replace("t_s144x90c5", "t_s1920x1080c5", 1)
        yield Request(url=item['url'], meta={'item': item})


class redisPipeline(object):
    def __init__(self, redis_url, redis_key):
        self.redis_url = redis_url
        self.redis_key = redis_key

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            redis_url=crawler.settings.get("REDIS_URL"),
            redis_key=crawler.settings.get("REDIS_KEY")
        )

    def open_spider(self, spider):
        self.db = redis.Redis.from_url(url=self.redis_url, db=1, decode_responses=True)

    def process_item(self, item, spider):
        score = int(item['yes']) - int(item['no'])
        print(score)
        name = item['folder_name']
        self.db.zadd(self.redis_key, name, score)

    def close_spider(self, spider):
        test.sendemail()
        # os.system("shutdown -s -t 300")







