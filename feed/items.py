# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FeedItem(scrapy.Item):
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


    product_id,store_id,brand,image_link,title,link,price,google_product_category,color,size,description,gender = scrapy.Field()

