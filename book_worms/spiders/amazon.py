# -*- coding: utf-8 -*-
import re

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

    blacklists = (
        "https://www.amazon.com/gp/*",

        )
    rules = [
        Rule(LinkExtractor(allow=('.*'), deny= blacklists), follow=True, callback="parse_items")
    ]

    def parse_items(self, response):
        book_title = response.selector.xpath('//div[contains(@id, "booksTitle")]')
        if book_title:
            item = BookWormsItem()
            print "#" * 100
            print response.url
            item['url'] = response.url
            item['title'] = response.selector.xpath('//h1[@id="title"]/span[1]/text()').extract()[0]
            authors = response.selector.xpath('//a[contains(@class, "contributorNameID")]/text()')
            if len(authors) > 0:
                authors = authors.extract()
            else:
                authors = response.selector.xpath('//span[contains(@class, "author")]/a/text()').extract()

            item['authors'] = authors

            genres = []

            unwanted_categories = ["Kindle"]

            categories = response.selector.xpath('//div[@id= "wayfinding-breadcrumbs_feature_div"]/ul/li/span/a/text()').extract()
            for category in categories:
                category = category.strip()
                add_flag = True
                for unwanted_category in unwanted_categories:
                    if unwanted_category in category:
                        add_flag = False
                        break

                if add_flag:
                    genres.append(category)

            item['genres'] = genres

            product_description_field = response.selector.xpath('//table[@id="productDetailsTable"]/tr/td/div/ul/li/b/text()').extract()
            product_description_value = response.selector.xpath('//table[@id="productDetailsTable"]/tr/td/div/ul/li/text()').extract()

            if "Paperback:" in product_description_field:
                index = product_description_field.index("Paperback:")
                item['pages'] = product_description_value[index].split()[0]
            elif "Print Length:" in product_description_field:
                index = product_description_field.index("Print Length:")
                item['pages'] = product_description_value[index].split()[0]

            if "Publisher:" in product_description_field:
                index = product_description_field.index("Publisher:")
                value = product_description_value[index]

                if ";" in value:
                    scolon_index = value.index(";")
                    item['publisher'] = value[:scolon_index]
                elif "(" in value:
                    b_index = value.index("(")

                    item['publisher'] = value[:b_index]

                item['year'] = re.search(r'\((.*?)\)', value).group(1)

            # print item
            # print "#" * 100
            return item