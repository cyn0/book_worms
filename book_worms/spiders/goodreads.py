# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from book_worms.items import BookWormsItem

class GoodReadSpider(CrawlSpider):
    name = 'goodreads'
    allowed_domains = ['goodreads.com']
    """
    1. 100 Books to Read in a Lifetime
    """
    start_urls = ['https://www.goodreads.com/list/show/7.Best_Books_of_the_21st_Century', 'https://www.goodreads.com/list/show/6.Best_Books_of_the_20th_Century']

    rules = [
        Rule(LinkExtractor(allow=('.*')), follow=True, callback="parse_items")
    ]

    def parse_items(self, response):
        book_title = response.selector.xpath('//div[contains(@id, "metacol")]')
        print("-----------------------------------------------------------------------")
        print()

        if book_title:
            item = BookWormsItem()

            #print response.selector.xpath('//div[@id = "metacol"]/text()').extract()[0]
            print()

            item['title'] = response.selector.xpath('//h1[@id = "bookTitle"]/text()').extract()[0].strip()
            item['authors'] = response.selector.xpath('//div[@id = "bookAuthors"]/span[@itemprop = "author"]/a/span/text()').extract()

            item['authorType'] = response.selector.xpath('//div[@id = "bookAuthors"]/span[@itemprop = "author"]/span/text()').extract()
            item['pages'] = response.selector.xpath('//div[@id = "details"]/div/span[@itemprop = "numberOfPages"]/text()').extract()

            item['isbn'] = response.selector.xpath(
                '//div[@id = "bookDataBox"]/div[contains(@class, "clearFloats")]/'
                'div[contains(@class, "infoBoxRowItem")]/text()').extract()[1].strip()

            item['isbn13'] = response.selector.xpath(
                '//div[@id = "bookDataBox"]/div[contains(@class, "clearFloats")]/'
                'div[contains(@class, "infoBoxRowItem")]/span/span/text()').extract()[0]

            item['language'] = response.selector.xpath('//div[@id = "bookDataBox"]/div[contains(@class, "clearFloats")]'
                                                       '/div[contains(@class, "infoBoxRowItem")]/text()').extract()[3]

            item['bookPublication'] = response.selector.xpath('//div[@id = "details"]/div[contains(@class, "row")]/'
                                                              'text()').extract()[1].strip().split()

            item['genres'] = response.selector.xpath('//div[contains(@class, "bigBoxContent containerWithHeaderContent")]'
                                                     '/div[contains(@class, "elementList")]/div[contains(@class, "left")]'
                                                     '/a/text()').extract()

            print(item)
            print()
            print("-----------------------------------------------------------------------")