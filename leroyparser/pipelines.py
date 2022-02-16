# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient


class LeroyparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.leroy

    def process_item(self, item, spider):
        try:
            item['price'] = int(item['price'].replace(' ', ''))
        except:
            item['price'] = None

        collection = self.mongobase[spider.search]
        collection.insert_one(item)

        return item


class LeroyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['images']:
            for image in item['images']:
                try:
                    yield scrapy.Request(image)
                except Exception as err:
                    print(err)

    def item_completed(self, results, item, info):
        item['images'] = [itm[1] for itm in results if itm[0]]

        return item
