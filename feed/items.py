# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# -*- This represents a JSON Object that will enter the database -*-
class FeedItem(scrapy.Item):
    # formats a category into normalized format
    # @parameter cats: String
    # @returns price: Float
    def to_google_taxonomy(cats):
        with open('./cats.csv', 'rb') as csvfile:
            catreader = csv.reader(csvfile, delimiter=';')
            
            google_taxonomy_code = None
            
            for row in catreader:
                if row[0].lower() in cats:
                    google_taxonomy_code =  row[1]
                    
            return google_taxonomy_code
                    
    # formats price into normalized format
    # @parameter price: String or Int 
    # @returns price: Float
    def parse_price(price):
        return "{0:.2f}".format(float(price) / 100.00)
                        
    product_id = scrapy.Field()
    store_id = scrapy.Field()
    brand = scrapy.Field()
    image_link = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    google_product_category = scrapy.Field()
    color = scrapy.Field()
    size = scrapy.Field()
    description = scrapy.Field()
    description_legacy = scrapy.Field()
    gender = scrapy.Field()
