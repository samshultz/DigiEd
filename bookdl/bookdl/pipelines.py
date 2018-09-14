# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from shop.models import Book, Category
import datetime

class BookdlPipeline(object):
    def process_item(self, item, spider):
        try:
            book = Book.objects.get(title=item['title'])
            print("Book already exists")
            return item
        except Book.DoesNotExist:
            pass
        c = Category.objects.filter(name=item['category'])
        if not c:
            cat = Category.objects.create(name=item['category'])
            cat = Category.objects.get(name=item['category'])
        else:
            cat = Category.objects.get(name=item['category'])
        
        book = Book()
        book.title = item['title']
        book.author = item['author']
        book.image_url = item['image_url']
        book.book_url = item['book_url']
        book.description = item['description']
        book.year = datetime.date(int(item['year']), 1, 1)
        book.num_pages = item['num_pages']
        book.publisher = item['publisher']
        book.isbn = item['isbn']
        book.file_format = item['file_format']
        book.price = item['price']
        book.category = cat
        
        book.save()
        book.tags.add(item['category'].lower())
        return item
