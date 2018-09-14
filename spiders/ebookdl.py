import random
import scrapy
from shop.models import Category, Book


class EbookSpider(scrapy.Spider):
    name = "ebook"
    start_urls = [
        'http://ebook-dl.com/cat/1',
    ]

    def parse(self, response):
        for ebook in response.css('div.four.shop.columns'):
            detail_page = "http://ebook-dl.com" + ebook.css("figure a::attr(href)").extract_first()

            yield response.css(detail_page, self.get_detail)

        next_page = response.css("a.next::attr(href)").extract_first()
        if next_page is not None:
            next_page = "http://ebook-dl.com" + response.css("a.next::attr(href)").extract_first()
            yield response.follow(next_page, self.parse)

    def get_detail(self, response):
        # Don't forget to set the category
        # don't forget to set the tags
        cat = response.css("#breadcrumbs > ul:nth-child(1) > li:last-child > a:nth-child(1)::text").extract_first()
        c = Category.objects.filter(name=cat)
        if not c:
            cat = Category.objects.create(name=cat)
            cat = Category.objects.get(name=cat)
        else:
            cat = Category.objects.get(name=cat)

        price_list = [1000, 1200, 1500, 2000]
        yr, pg, pub, lang, isbn, file_size, file_format, *other = response.css("table.basic-table td::text").extract()
        
        fields = {
            'category': cat,
            'title': response.css("section.titlebar h1::text").extract_first().strip(),
            'author': response.css("table.basic-table h2::text").extract_first(),
            'image_url': response.css(".mfp-image > img::attr(src)").extract_first(),
            'book_url': "http://ebook-dl.com" + response.css("section.linking > a.button.adc::attr(href)").extract_first(),
            'description': response.css("p.margin-reset::text").extract_first(),
            'year': yr,
            'num_pages': pg,
            'publisher': pub,
            'isbn': isbn,
            'file_format': file_format,
            
            }
        if int(fields['num_pages']) > 200:
            fields['price'] = random.choice(price_list)
        book = Book(fields)
        book.tags.add(str(cat).lower())
        book.save()
        return fields