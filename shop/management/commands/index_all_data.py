from django.core.management import BaseCommand

import elasticsearch_dsl
import elasticsearch_dsl.connections
from shop.es_docs import ESBook
from shop.models import Book


class Command(BaseCommand):
    help = "Index all data to Elasticsearch"
    def handle(self, *args, **options):
        elasticsearch_dsl.connections.connections.create_connection(hosts=['https://ef45e787737c2385b89f93820c9bfea6.us-east-1.aws.found.io'])
        for book in Book.objects.all():
            if book.image:
                image = book.image.url
            else:
                image = book.image_url
            
            if book.book_file:
                download_link = book.book_file.url
            else:
                download_link = book.book_url

            esp = ESBook(meta={'id': book.pk},
                     title=book.name,
                     image=image,
                     url=book.get_absolute_url(),
                     price=book.price,
                     publisher=book.publisher,
                     author=book.author,
                     download_link=download_link

                     )
        
        
            esp.save(index='books')
        