# -*- coding: utf-8 -*-

import scrapy
import urlparse
import re
from time import gmtime, strftime
from bookstoscrape.items import BookItem

class BookSpider(scrapy.Spider):
    name = 'bookspider'
    allowed_domains = ["toscrape.com"]
    start_urls = ['http://books.toscrape.com/index.html']
    

    def parse(self, response):

	#let's grab the elements that contain the book page links and thumbnails for the book
	product_containers = response.css('.product_pod > div > a')
	
	#now let's loop through the elements and get each book page link and thumbnail
	for product in product_containers:
	    link = product.xpath('@href').extract_first()

	    #we're passing the thumbnail URL to next function (parse_item) with the meta argument. This is yield with the request - then we can later process it as an item field. Scrapy is able to generate thumbnails from bigger sized images it downloads, but we're downloading the thumbnail directly for the sake of showcasing the meta argument.

	    thumbnail_url = product.xpath('img/@src').extract_first()
	    yield scrapy.Request(response.urljoin(link.strip()), callback=self.parse_item, meta={'thumbnail_url': thumbnail_url})

	#we check if there's a link for a next page, and if there is one, we come back to the parse function so we can yield more book pages link requests (books that show on the next pages)
	next_page = response.xpath('//li[@class="next"]/a/@href').extract_first()
	if next_page is not None:
	    yield scrapy.Request(response.urljoin(next_page), callback=self.parse)


    def parse_item(self, response):
	item = BookItem()


	#using the selectors to grab the information we need. If we use CSS like we did initially above, Scrapy actually treats it as Xpath under the hood as mentioned in Scrapy's documentation
	title = response.xpath("//div[contains(@class, 'product_main')]/h1/text()").extract_first().strip()
	item['title']= title

	parsed_uri = urlparse.urlparse(response.url)
	domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
	thumbnail_url = response.meta['thumbnail_url']
	item['thumbnail'] = domain + thumbnail_url
	
	#a timestamp for when the item was scraped
	data_modified = strftime("%Y-%m-%d %H:%M:%S", gmtime())
	item['data_modified'] = data_modified
	
	category = response.xpath('//ul[@class="breadcrumb"]/li[3]/a/text()').extract_first().strip()
	item['category'] = category

	description = response.xpath("//div[@id='product_description']/following-sibling::p/text()").extract_first().strip()
	item['description'] = description

	upc = response.xpath("//tr[th/text()='UPC']/td/text()").extract_first().strip()
	item['upc'] = upc

	price_no_tax = response.xpath("//tr[th/text()='Price (excl. tax)']/td/text()").extract_first().strip()
        item['price_no_tax'] = price_no_tax
	
	price_tax = response.xpath("//tr[th/text()='Price (incl. tax)']/td/text()").extract_first().strip()
	item['price_tax'] = price_tax
	
	product_type = response.xpath("//tr[th/text()='Product Type']/td/text()").extract_first().strip()
	item['product_type'] = product_type

	availability = response.xpath("//tr[th/text()='Availability']/td/text()").extract_first().strip()
	item['availability'] = availability 

	reviews_nr = response.xpath("//tr[th/text()='Number of reviews']/td/text()").extract_first().strip()
	item['reviews_nr'] = reviews_nr
	
	item['image_result'] = []
	item['images'] = []
	image_response = response.xpath("//div[contains(@class, 'item')]/img/@src").extract()

	#There's only one image per book page, but if there were more we could get them like so:
	for elem in image_response:
	    item['images'].append(response.urljoin(elem.strip()))

	yield item
	
	
