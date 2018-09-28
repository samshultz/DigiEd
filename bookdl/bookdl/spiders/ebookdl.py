# -*- coding: utf-8 -*-
import scrapy
from bookdl.items import BookdlItem
import random

class EbookdlSpider(scrapy.Spider):
    name = 'ebookdl'
    allowed_domains = ['ebook-dl.com']
    start_urls = ['http://ebook-dl.com/cat/1']

    def parse(self, response):
        for ebook in response.css('div.four.shop.columns'):
            detail_page = "http://ebook-dl.com" + ebook.css("figure a::attr(href)").extract_first()

            yield response.follow(detail_page, self.get_detail)

        next_page = response.css("a.next::attr(href)").extract_first()
        if next_page is not None:
            next_page = "http://ebook-dl.com" + response.css("a.next::attr(href)").extract_first()
            yield response.follow(next_page, self.parse)

    def get_detail(self, response):
        # Don't forget to set the category
        # don't forget to set the tags
        item = BookdlItem()
        cat = response.css("#breadcrumbs > ul:nth-child(1) > li:last-child > a:nth-child(1)::text").extract_first()
        

        price_list = [1000, 1200, 1500, 2000]
        yr, pg, pub, lang, isbn, file_size, file_format, *other = response.css("table.basic-table td::text").extract()
        
        item['category'] = cat
        item['title'] = response.css("section.titlebar h1::text").extract_first().strip()
        item['author'] = response.css("table.basic-table h2::text").extract_first()
        item['image_url'] = response.css(".mfp-image > img::attr(src)").extract_first()
        item['book_url'] = "http://ebook-dl.com" + response.css("section.linking > a.button.adc::attr(href)").extract_first()
        item['description'] = response.css("p.margin-reset::text").extract_first()
        item['year'] = yr
        item['num_pages'] = pg
        item['publisher'] = pub
        item['isbn'] = isbn
        item['file_format'] = file_format
            
        if int(item['num_pages']) > 300:
            item['price'] = random.choice(price_list)
        
        return item


class AllItebooksSpider(scrapy.Spider):
    name = 'allitebooks'
    allowed_domains = ['allitebooks.com']
    start_urls = ['http://www.allitebooks.com/']

    def parse(self, response):
        for ebook in response.css("article > div:nth-child(2) > header:nth-child(1) > h2:nth-child(1) > a:nth-child(1)::attr(href)").extract():

            yield response.follow(ebook, self.get_detail)

        num_pages = int(response.css(".pages::text").extract_first().split()[2])
        current_page = int(response.css(".current::text").extract_first())
        if current_page < num_pages:
            next_page = "http://www.allitebooks.com/page/{}/".format(current_page + 1)
            yield response.follow(next_page, self.parse)

    def get_detail(self, response):
        # Don't forget to set the category
        # don't forget to set the tags
        categories = {'Datebases': "Databases & Big Data",
                      'Web Development': "Web Development & Design", 
                      'Administration': "Administration",
                      'Computers & Technology': "Computer Science", 
                      "Enterprise": "Enterprise",
                      'Game Programming': "Games & Strategy Guides", 
                      'Marketing & SEO': "Marketing & SEO",
                      'Security': "Security & Encryption"}
        item = BookdlItem()
        cat = response.css(".book-detail > dl:nth-child(1) > dd:nth-child(16) > a:nth-child(1)::text").extract_first()
        cat = categories.get(cat, cat)


        price_list = [300, 500, 700]
        
        item['category'] = cat
        item['title'] = response.css(".single-title::text").extract_first().strip()
        item['author'] = response.css(".book-detail > dl:nth-child(1) > dd:nth-child(2) > a:nth-child(1)::text").extract_first().strip()
        item['image_url'] = response.css(".attachment-post-thumbnail::attr(src)").extract_first().strip()
        item['book_url'] = response.css("span.download-links:nth-child(1) > a:nth-child(1)::attr(href)").extract_first().strip()
        item['description'] = response.css(".entry-content p::text").extract_first().strip()
        item['year'] = response.css(".book-detail > dl:nth-child(1) > dd:nth-child(6)::text").extract_first().strip()
        item['num_pages'] = response.css(".book-detail > dl:nth-child(1) > dd:nth-child(8)::text").extract_first().strip()
        item['publisher'] = ""
        item['isbn'] = response.css(".book-detail > dl:nth-child(1) > dd:nth-child(4)::text").extract_first().strip()
        item['file_format'] = response.css(".book-detail > dl:nth-child(1) > dd:nth-child(14)::text").extract_first().strip()
            
        if int(item['num_pages']) > 300:
            item['price'] = random.choice(price_list)
        
        return item