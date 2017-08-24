# -*- coding: utf-8 -*-
from scrapy import signals
from scrapy.exporters import XmlItemExporter
from scrapy.exporters import BaseItemExporter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from bookstoscrape.items import BookItem
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class FirstPipeline(object):
    def process_item(self, item, spider):
        return item


class XmlExportPipeline(object):

    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
         pipeline = cls()
         crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
         crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
         return pipeline

    def spider_opened(self, spider):
        file = open('%s_adverts.xml' % spider.name, 'w+b')
        self.files[spider] = file
        self.exporter = XmlItemExporter(file)
	self.exporter.root_element = 'books'
	self.exporter.item_element = 'book'
        self.exporter.fields_to_export = ['title', 'upc', 'category','data_modified', 'price_tax', 'price_no_tax','tax','availability', 'reviews_nr','description', 'product_type', 'thumbnail', 'images']
        self.exporter.start_exporting()



    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()
	

    def process_item(self, item, spider):
	self.exporter.export_item(item)
        return item
	
class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item




