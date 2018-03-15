# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from book_worms.items import BookWormsItem

class AmazonSpider(CrawlSpider):
    name = 'amazon'
    allowed_domains = ['amazon.com']
    """
    1. 100 Books to Read in a Lifetime
    """
    start_urls = ['https://www.amazon.com/b/ref=s9_acss_bw_cg_BHPJAN_1c1_w?node=8192263011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-2&pf_rd_r=FR7SMMBC7C9SWA46989S&pf_rd_t=101&pf_rd_p=d4740385-a7ba-4621-95a2-c96f66a01084&pf_rd_i=283155']

    rules = [
        Rule(LinkExtractor(allow=('.*')), follow=True, callback="parse_items")
    ]

    def parse_items(self, response):
        book_title = response.selector.xpath('//div[contains(@id, "booksTitle")]')
        if book_title:
            item = BookWormsItem()
            print "#" * 100
            print response.url
            print response.selector.xpath('//title/text()').extract()[0]
            item['title'] = response.selector.xpath('//span[@id="productTitle"]/text()').extract()[0]
            item['authors'] = response.selector.xpath('//a[contains(@class, "contributorNameID")]/text()').extract()[0]

            categories = response.selector.xpath('//li/span/a[contains(@class,"a-color-tertiary")]/text()')
            genres = []
            for category in categories:
                category.extract().strip()
            item['genres'] = genres
            print item
            print "#" * 100