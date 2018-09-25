from django.contrib.sitemaps import Sitemap
from .models import Book

class BookSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        return Book.objects.all()

    def lastmod(self, obj):
        return obj.updated