# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import re
import scrapy
from scrapy.item import Item, Field

#function to remove the £ symbol on the price field and keep the number (digits with commas and dots) with regex
def serialize_field(value):
	trim = re.compile(r'[^\d.,]+')
	result = trim.sub('', value)
        return result


class BookItem(scrapy.Item):
    
    # define the fields for your item (book) here like:
    upc = scrapy.Field()
    thumbnail = scrapy.Field()
    title = scrapy.Field()
    category = scrapy.Field()
    product_type = scrapy.Field()
    price_no_tax = scrapy.Field(serializer=serialize_field)
    price_tax = scrapy.Field(serializer=serialize_field)
    tax = scrapy.Field(serializer=serialize_field)
    availability = scrapy.Field()
    reviews_nr = scrapy.Field()
    data_modified = scrapy.Field()
    description = scrapy.Field()
    images = scrapy.Field()
    image_result = scrapy.Field()
