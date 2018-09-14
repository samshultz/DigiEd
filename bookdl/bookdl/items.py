# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookdlItem(scrapy.Item):
    # define the fields for your item here like:
    category = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    image_url = scrapy.Field()
    book_url = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    year = scrapy.Field()
    num_pages = scrapy.Field()
    publisher = scrapy.Field()
    isbn = scrapy.Field()
    file_format = scrapy.Field()