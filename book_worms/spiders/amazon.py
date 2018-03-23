# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from book_worms.items import BookWormsItem

import pdb

class AmazonSpider(CrawlSpider):
    name = 'amazon'
    allowed_domains = ['amazon.com']
    """
    1. 100 Books to Read in a Lifetime
    """
    start_urls = [

        # 'https://www.amazon.com/b/ref=amb_link_1?ie=UTF8&node=17296221011',
        # 'https://www.amazon.com/Books/b?ie=UTF8&node=549028',
        # 'https://www.amazon.com/b/ref=bhp_brws_awrd?ie=UTF8&node=6960520011&pf_rd_m=ATVPDKIKX0DER'
        # 'https://www.amazon.com/b/ref=s9_acss_bw_cg_BHPJAN_1c1_w?node=8192263011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-2&pf_rd_r=FR7SMMBC7C9SWA46989S&pf_rd_t=101&pf_rd_p=d4740385-a7ba-4621-95a2-c96f66a01084&pf_rd_i=283155',
        #top mysteries to read in lifetime
        # "https://www.amazon.com/b/ref=amb_link_6?ie=UTF8&node=8994558011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-leftnav&pf_rd_r=ZVHGGYH9E20WDXXXS9M1&pf_rd_r=ZVHGGYH9E20WDXXXS9M1&pf_rd_t=101&pf_rd_p=1098fb88-f951-4c94-bb1d-aa7bb0f59198&pf_rd_p=1098fb88-f951-4c94-bb1d-aa7bb0f59198&pf_rd_i=8192263011",
        # 100 scifi & fantasy
        # "https://www.amazon.com/100-Science-Fiction-Fantasy-Books-to-Read-in-a-Lifetime/b/ref=amb_link_3?ie=UTF8&node=12661600011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-leftnav&pf_rd_r=QJJ9K804FJ2BHCRK8BT5&pf_rd_r=QJJ9K804FJ2BHCRK8BT5&pf_rd_t=101&pf_rd_p=33369655-1894-4c23-829e-85cf931543fb&pf_rd_p=33369655-1894-4c23-829e-85cf931543fb&pf_rd_i=8994558011"
        # 100 children books
        # "https://www.amazon.com/b/ref=amb_link_2?ie=UTF8&node=9660210011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-leftnav&pf_rd_r=FVFCNWQVYXQ9TMVMTD91&pf_rd_r=FVFCNWQVYXQ9TMVMTD91&pf_rd_t=101&pf_rd_p=f1010d03-0341-42c6-89f6-c0694e53345e&pf_rd_p=f1010d03-0341-42c6-89f6-c0694e53345e&pf_rd_i=12661600011"
    ]

    # for i in range(1,6):
    #     url = "https://www.amazon.com/best-sellers-books-Amazon/zgbs/books/ref=zg_bs_pg_2/141-0080878-3910661?_encoding=UTF8&pg=%s" % (i,)
    #     start_urls.append(url)

    # for i in range(1, 8):
    #     url = "https://www.amazon.com/gp/search/?srs=17296221011&page=%s" %(i, )
    #     start_urls.append(url)

    for i in range(1, 6):
        # url = "https://www.amazon.com/best-sellers-books-Amazon/zgbs/books/ref=zg_bs_unv_b_1_10159402011_3#%s"%(i,)
        # url = "https://www.amazon.com/Best-Sellers-Books-Science-Fiction-Fantasy/zgbs/books/25/ref=zg_bs_nav_b_1_b#%s"%(i, )
        # url = "https://www.amazon.com/Best-Sellers-Books-Science-Math/zgbs/books/75/ref=zg_bs_nav_b_1_b#%s"% (i, )
        # url = "https://www.amazon.com/Best-Sellers-Books-Fantasy/zgbs/books/16190/ref=zg_bs_nav_b_2_25#%s" % (i,)
        # url = "https://www.amazon.com/Best-Sellers-Books-Mystery-Thriller-Suspense/zgbs/books/18/ref=zg_bs_nav_b_1_b#%s" % (i,)
        url = "https://www.amazon.com/Best-Sellers-Books-Childrens/zgbs/books/4/ref=zg_bs_nav_b_1_b#%s" % (i, )
        start_urls.append(url)
        # url = "https://www.amazon.com/Best-Sellers-Books-Business-Money/zgbs/books/3/ref=zg_bs_nav_b_1_b#%s" % (i,)
        url = "https://www.amazon.com/Best-Sellers-Books-Literature-Fiction/zgbs/books/17/ref=zg_bs_nav_b_1_b#%s" % (i, )
        start_urls.append(url)
        # url = "https://www.amazon.com/Best-Sellers-Books-Travel/zgbs/books/27/ref=zg_bs_nav_b_1_b#%s" % (i,)
        url = "https://www.amazon.com/Best-Sellers-Books-Parenting-Relationships/zgbs/books/20/ref=zg_bs_nav_b_1_b#%s" % (i, )
        start_urls.append(url)
    # for i in range(1,5):
    #     url = "https://www.amazon.com/Best-Sellers-Books-Romance/zgbs/books/23/ref=zg_bs_nav_b_1_b#%s" % (i,)
    #     start_urls.append(url)
    blacklists = (
        "/*\/gp/*",
        "/*reviews/*",
        "/*gift/*",
        "/*Gift/*",
        "/*stream/*",
        "\/e\/",
        "\/services\/",
        "/*zgbs/*",
        "/*\/b\?/*",
        "chart",
        "/*/s\/",
        "/*credit/*"
        )

    rules = [
        Rule(LinkExtractor(allow=('.*'), deny=blacklists), follow=True, callback="parse_items")
    ]

    def parse(self, response):
        # links = response.selector.xpath("//a[@class='a-link-normal']/@href").extract()
        links = response.selector.xpath("//div[@id='zg_left_colmask']//a/@href").extract()
        for link in links:
            yield scrapy.Request("https://www.amazon.com" + link, callback=self.parse_items)

    def is_book(self, response):
        book_title = response.selector.xpath('//div[contains(@id, "booksTitle")]')
        if book_title:
            return True

        category_div = response.selector.xpath('//div[@id= "wayfinding-breadcrumbs_feature_div"]/ul/li/span/a/text()').extract()
        if len(category_div) > 0 and category_div[0].strip() == 'Books':
            return True
        if response.url == "https://www.amazon.com/Woman-Window-Novel-J-Finn/dp/0062678418":
            pdb.set_trace()
        if response.url == "https://www.amazon.com/Lorax-Classic-Seuss-Dr/dp/0394823370":
            pdb.set_trace()
        if response.url == "https://www.amazon.com/Where-Sidewalk-Ends-Poems-Drawings/dp/0060256672":
            pdb.set_trace()
        print "$"*100
        print response.selector.xpath('//title/text()').extract()[0]
        print response.url
        print category_div
        print "$"*100
        return False

    def parse_items(self, response):
        if self.is_book(response):
            item = BookWormsItem()
            #print "#" * 100
            #print response.url
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

                item['publisher'] = item['publisher'].replace("  ", " ")
                item['year'] = re.search(r'\((.*?)\)', value).group(1)

            if "Language:" in product_description_field:
                index = product_description_field.index("Language:")
                value = product_description_value[index]

                item['language'] = value

            if "ISBN-10:" in product_description_field:
                index = product_description_field.index("ISBN-10:")
                value = product_description_value[index]

                item['isbn'] = value

            if "ISBN-13:" in product_description_field:
                index = product_description_field.index("ISBN-13:")
                value = product_description_value[index]

                item['isbn13'] = value

            # print item
            # print "#" * 100
            return item

        else:
            pass
            # print "~"*100
            # print "ignored"
            # print response.selector.xpath('//title/text()').extract()[0]
            # print response.url
            # print "~"*100
