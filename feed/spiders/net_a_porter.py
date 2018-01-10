# -*- coding: utf-8 -*-
from scrapy.spiders import SitemapSpider
from ..items import FeedItem
import csv, re

class NetAPorterSpider(SitemapSpider):
    first = "{&quot;size&quot;:&quot;"
    last = "&quot;,&quot;stock&quot;:&quot;In_Stock"
    name = "net-a-porter"
    sitemap_urls = ['https://www.net-a-porter.com/us.en.sitemap2.xml']
    sitemap_rules = [
        ('product', 'parse_product')
    ]



    def parse_product(self,response):
        if 'http://schema.org/InStock' in ''.join(response.xpath('//link[@itemprop="availability"]//@href').extract()):
            item = FeedItem()
            item['link'] = response.url
            item['product_id'] = response.xpath('//@data-pid').extract()[0]
            item['store_id'] = item['product_id']
            item['title'] = ''.join(response.xpath('//title/text()').extract()).replace("| NET-A-PORTER.COM","")
            item['description_legacy'] = {
                'text': response.xpath('//meta[@name="description"]/@content')
                    .extract()[0],
                'bullets': filter(None, map((lambda x: x.strip().replace('- ','')),
                                            response.xpath('//ul[@class="font-list-copy"]//li//text()').extract()
                                            ))
            }

            item['description'] = item['description_legacy']['text'] + " - " \
                                  + ''.join(filter(None, map((lambda x: x.strip()),
                                            response.xpath('//ul[@class="font-list-copy"]//li//text()').extract()
                                            )))

            response.xpath('//ul[@class="font-list-copy"]//li//text()').extract()

            cats = response.xpath('//meta[@class="product-data"]/@data-breadcrumb-keys').extract()[0]\
                .lower()\
                .replace(' ', '')\
                .split('/')

            for cat in cats:
                cat.lower()

            def parse_price(price):
                return "{0:.2f}".format(float(price) / 100.00)

            price = response.xpath('//meta[@class="product-data"]/@data-price').extract()[0]

            item['price'] = parse_price(price)

            with open('./cats.csv', 'rb') as csvfile:
                catreader = csv.reader(csvfile, delimiter=';')

                for row in catreader:
                    if row[0].lower() in cats:
                        item['google_product_category'] = row[1]

            item['brand'] = ''.join(response.xpath('//span[@itemprop="name"]//text()').extract())

            item['image_link'] = 'http:' + ''.join(response.xpath('//meta[@itemprop="image"]/@content').extract())

            item['gender'] = "female"

            sizes = ''.join(response.xpath('//*[@label="Choose your size"]/@options').extract())

            size = None

            if sizes:
                size = re.search(self.first + '(.*)', self.last)
            else:
                size = "N.A"

            if size:
                item['size'] = size

            item['color'] = ''.join(response.xpath('//*[@name="Editor\'s Notes"]//ul/li[1]/text()')
                .extract())\
                .replace('-', '')\
                .strip()

            yield item

        else:
            pass