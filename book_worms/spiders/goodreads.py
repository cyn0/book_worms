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
    start_urls = []
    for i in range(81):
        link = 'https://www.goodreads.com/list/show/7.Best_Books_of_the_21st_Century?page=' + str(i + 1)
        start_urls.append(link)

    black = ("\*list\*", )
    rules = [
        Rule(LinkExtractor(allow=('.*'), deny = black), follow=True, callback="parse_items")
    ]

    def parse_items(self, response):
        book_title = response.selector.xpath('//div[contains(@id, "metacol")]')
        #print("-----------------------------------------------------------------------")
        #print()

        if book_title:
            item = BookWormsItem()

            #print response.selector.xpath('//div[@id = "metacol"]/text()').extract()[0]
            #print()

            item['title'] = response.selector.xpath('//h1[@id = "bookTitle"]/text()').extract()[0].strip()
            item['authors'] = response.selector.xpath('//div[@id = "bookAuthors"]/span[@itemprop = "author"]/a/span/text()').extract()

            authors = item['authors']
            new_authors = list()
            for val in authors:
                new_authors.append(val.strip())
            item['authors'] = new_authors

            #item['authorType'] = response.selector.xpath('//div[@id = "bookAuthors"]/span[@itemprop = "author"]/span/text()').extract()

            item['pages'] = response.selector.xpath('//div[@id = "details"]/div/span[@itemprop = "numberOfPages"]/text()').extract()[0].split()[0]

            item['isbn'] = response.selector.xpath(
                '//div[@id = "bookDataBox"]/div[contains(@class, "clearFloats")]/'
                'div[contains(@class, "infoBoxRowItem")]/text()').extract()[1].strip()

            item['isbn13'] = response.selector.xpath(
                '//div[@id = "bookDataBox"]/div[contains(@class, "clearFloats")]/'
                'div[contains(@class, "infoBoxRowItem")]/span/span/text()').extract()[0].strip()

            item['language'] = response.selector.xpath('//div[@id = "bookDataBox"]/div[contains(@class, "clearFloats")]'
                                                       '/div[contains(@class, "infoBoxRowItem")]/text()').extract()[3].strip()

            publication = response.selector.xpath('//div[@id = "details"]/div[contains(@class, "row")]/'
                                                    'text()').extract()

            splitted = []
            for i in publication:
                if 'Published' in i:
                    splitted = i.split('\n')

            s = ''
            for i in splitted:
                if 'by' in i:
                    string_split = i.strip().split(' ')

            for i in string_split:
                if not 'by' in i:
                    s = s + i + ' '

            item['publisher'] = s.strip()

            months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                      'November', 'December']
            found = False
            pub_year = ''

            for i in splitted:
                for month in months:
                    if month in i:
                        pub_year = i
                        found = True
                        break

                if found:
                    break

            item['year'] = pub_year.strip()

            item['genres'] = response.selector.xpath('//div[contains(@class, "bigBoxContent containerWithHeaderContent")]'
                                                     '/div[contains(@class, "elementList")]/div[contains(@class, "left")]'
                                                     '/a/text()').extract()
            genres = item['genres']
            new_genres = list()
            for val in genres:
                new_genres.append(val.strip())
            item['genres'] = new_genres

            item['url'] = response.url

            #print(item)
            #print()
            #print("-----------------------------------------------------------------------")
            return item