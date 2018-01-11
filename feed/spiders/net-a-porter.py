# -*- coding: utf-8 -*-
from scrapy.spiders import SitemapSpider
from ..items import FeedItem
import csv, re
# Build class from scrapy.spiders
class NetAPorterSpider(SitemapSpider):
    #  give the crawler a name 
    name = "net-a-porter"
    # provide path to the sitemap xml 
    sitemap_urls = ['https://www.net-a-porter.com/us.en.sitemap2.xml']
    
    # provide the rules (if the xml contains the string product the retrieve the html and parse it 
    sitemap_rules = [
        ('product', 'parse_product')
    ]

    # provide the xpath or css to each item in FeedItem which is the model created in items.py
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
            
            # extract the categories from the html and use to_google_taxonomy to convert to google taxonomy 
            cats = response.xpath('//meta[@class="product-data"]/@data-breadcrumb-keys').extract()[0]\
                .lower()\
                .replace(' ', '')\
                .split('/')
                
            item['google_product_category'] = item.to_google_taxonomy(cats)

            item['price'] = item.parse_price(response.xpath('//meta[@class="product-data"]/@data-price').extract()[0])

            item['brand'] = ''.join(response.xpath('//span[@itemprop="name"]//text()').extract())

            item['image_link'] = 'http:' + ''.join(response.xpath('//meta[@itemprop="image"]/@content').extract())

            item['gender'] = "female"

            item['color'] = ''.join(response.xpath('//*[@name="Editor\'s Notes"]//ul/li[1]/text()')
                .extract())\
                .replace('-', '')\
                .strip()

            yield item

        else:
            pass
