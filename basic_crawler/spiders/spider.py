from scrapy.spiders import BaseSpider
from scrapy.selector import Selector
from basic_crawler.items import BasicCrawlerItem
from scrapy.http import Request

class MySpider(BaseSpider):

    name = "basic_crawler" # crawler name
    allowed_domains = ['packtpub.com'] # targets
    start_urls = ['https://www.packtpub.com'] #start URL

    def parse(self, response):
        hxs = Selector(response) # parsing of the results to an selector

        # cross path query -> based on analysis of div
        book_titles = hxs.xpath('//div[@class="book-block-title"]/text()').extract()
        # iterating titles and creating Items Objects
        for title in book_titles:
            book = BasicCrawlerItem() # creating Item (items.py)
            book["title"] = title # assignation
            yield book
