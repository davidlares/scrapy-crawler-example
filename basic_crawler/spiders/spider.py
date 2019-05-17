from scrapy.spiders import BaseSpider
from scrapy.selector import Selector
from basic_crawler.items import BasicCrawlerItem
from scrapy.http import Request
import re

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

        # checking links
        visited_links=[]
        links = hxs.xpath('//a/@href').extract()
        # regex for http and https
        link_validator= re.compile("^(?:http|https):\/\/(?:[\w\.\-\+]+:{0,1}[\w\.\-\+]*@)?(?:[a-z0-9\-\.]+)(?::[0-9]+)?(?:\/|\/(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+))?$")

        # iterating links
        for link in links:
        	if link_validator.match(link) and not link in visited_links: # absolute URL and not visited
        		visited_links.append(link)
        		yield Request(link, self.parse)
        	else:
        		full_url=response.urljoin(link)
        		visited_links.append(full_url) # creating an absolute URL
        		yield Request(full_url, self.parse)

        # Scraping Forms
		forms = hxs.xpath('//form/@action').extract()
		for form in forms:
			form_item = BasicCrawlerItem()
			form_item["form"] = form
			form_item["location_url"] = response.url
			yield form_item

		# Scraping emails
		emails = hxs.xpath("//*[contains(text(),'@')]").extract()
		for email in emails:
			e = BasicCrawlerItem()
			e["email"] = email
			e["location_url"] = response.url
			yield e

		# Scraping comments
		comments = hxs.xpath('//comment()').extract()
		for comment in comments:
			c = BasicCrawlerItem()
			c["comments"] = comment
			c["location_url"] = response.url
			yield c
