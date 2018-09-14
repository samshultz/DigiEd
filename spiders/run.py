from scrapy.crawler import CrawlerProcess
from spiders.ebookdl import EbookSpider

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(EbookSpider)
process.start()