# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from collections import OrderedDict
import csv

class bulkmroComSpider(scrapy.Spider):

	name = "bulkmro_com_spider_test1"

	start_urls = ['http://www.bulkmro.com/']
	domain = 'http://www.bulkmro.com'
	total_count = 0

	def __init__(self, *args, **kwargs):
		super(bulkmroComSpider, self).__init__(*args, **kwargs)
###########################################################
	def start_requests(self):
		yield Request('https://www.bulkmro.com/all-categories', callback=self.parse_category)

	# get category
	def parse_category(self, response):
		exist_sub_cat_list = []
		f2 = open('bulkmro_com_result_other_2.csv')

		csv_items = csv.DictReader(f2)

		for i, row in enumerate(csv_items):
			v = row['current_ppage_link']
			if not (v in exist_sub_cat_list):
				exist_sub_cat_list.append(v)
				yield Request(v, callback=self.parse_products, dont_filter=True)
			# break
		#
		# xpaths_for_all_category = response.xpath('//*[@class="sub-category"]/li/ul/li')
		# sub_category_href_list = []
		# for xpath_category in xpaths_for_all_category:
		# 	if not xpath_category.xpath('.//@style').extract_first():
		# 		href = xpath_category.xpath('.//a/@href').extract_first()
		# 		sub_category_href_list.append(href)
		#
		#
		#
		# j = 0
		# for sub_category_href in sub_category_href_list:
		# 	if j > 1000:
		# 		break
		#
		# 	com = sub_category_href.split('/')[-1].split('.')[0]
		#
		# 	if not (com in exist_sub_cat_list):
		# 		yield Request(sub_category_href, callback=self.parse_products, dont_filter=True)
		#
		# 	j += 1





	def parse_products(self, response):
		# result_item = OrderedDict()
		# result_item['category'] = response.meta['category']
		# result_item['sub-category'] = response.meta['sub-category']
		# result_item['sub-sub-category'] = response.meta['sub-sub-category']
		# result_item['product name'] = response.meta['product name']
		# result_item['manufacture name'] = response.meta['manufacture name']
		# result_item['product id'] = response.meta['product id']
		# result_item['manufacture model number'] = response.meta['manufacture model number']
		# price = ''
		# price = response.xpath('.//*[contains(@id,"product-price")]/text()').re(r'[\d.,]+')
		# if not price:
		# 	price = response.xpath('.//*[contains(@id,"old-price")]/text()').re(r'[\d.,]+')
		# if not price:
		# 	price = response.xpath('.//*[@class="price"]/text()').re(r'[\d.,]+')
		# if price:
		# 	price = price[0].strip().replace(',', '')
		# result_item['price'] = price
		# result_item['link'] = response.meta['link']
		# try:
		# 	result_item['current_page_link'] = response.meta['current_ppage_link']
		# except:
		# 	result_item['current_page_link'] = ''
        #
		# self.total_count += 1
		# print('Total Count : {}'.format(str(self.total_count)))
        #
		# yield result_item
		xpaths_products = response.xpath('//*[@class="category-products"]/ul/li')
		category = response.xpath('//*[@class="breadcrumbs"]/ul/li[2]/a/text()').extract_first()
		sub_category = response.xpath('//*[@class="breadcrumbs"]/ul/li[3]/a/text()').extract_first()
		sub_sub_category = response.xpath('//*[@class="breadcrumbs"]/ul/li[4]/a/text()').extract_first()
		for xpath_product in xpaths_products:

			product_id = ''
			manufacture_model_number = ''

			for attr in xpath_product.xpath('.//*[@class="product-info"]/p/text()').extract():
				attr_name = attr.split(':')[0]
				if not attr_name:
					continue
				if attr_name.lower().__contains__('product'):
					product_id = attr.split(':')[1].strip()
				elif attr_name.lower().__contains__('mfr model'):
					manufacture_model_number = attr.split(':')[1].strip()

			price = ''
			price = xpath_product.xpath('.//*[contains(@id,"product-price")]/text()').re(r'[\d.,]+')
			if not price:
				price = xpath_product.xpath('.//*[contains(@id,"old-price")]/text()').re(r'[\d.,]+')
			if not price:
				price = xpath_product.xpath('.//*[@class="price"]/text()').re(r'[\d.,]+')
			if price:
				price = price[0].strip().replace(',', '')

			result_item = OrderedDict()
			result_item['category'] = category
			result_item['sub-category'] = sub_category
			result_item['sub-sub-category'] = sub_sub_category
			result_item['product name'] = xpath_product.xpath('.//a/@title').extract_first()
			result_item['manufacture name'] = xpath_product.xpath('.//div/a/text()').extract_first()
			result_item['product id'] = product_id
			result_item['manufacture model number'] = manufacture_model_number
			result_item['price'] = price
			result_item['link'] = xpath_product.xpath('.//a/@href').extract_first()
			result_item['current_page_link'] = response.url

			self.total_count += 1
			print('Total Count : {}'.format(str(self.total_count)))

			yield result_item

		# next_href = response.xpath('//*[@class="next i-next"]/@href').extract_first()
		# if next_href:
		# 	yield Request(next_href, callback=self.parse_products, dont_filter=True)


