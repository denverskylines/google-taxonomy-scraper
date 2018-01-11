# Google Taxonomy Scraper
### Duas Americas Group, Inc
##### North: Boca Raton, FL USA  - Aslan Varoqua, CEO
##### South: Araras, São Paulo, BR Daniel Vieira, COO

This source is open and can be used freely and subject only to the terms in LICENSE (MIT)

## Overview

Google taxonomy scraper is used to crawl e-commerce websites and extract structured 
data from their pages. It then normalizes the data and categorizes them into a 
into Google's Taxonomy for use on Google Shopping.

## Usage

Match yours or any e-commerce sites categories to corrosponding google categories 
and place them into cats.csv in the following format:

```
Shoes;187
Dresses;2271
Clothing;1604
Bags;6551
Accessories;166
Pants:204
Day Dresses;2271
Evening Dresses;2271
Jeans;204
Tops;212
Skirts;1581
Pants;204
Knitwear;203
Jackets;203
Coats;203
Swimwear;211
Clutch;6551
```

then

scrapy crawl {retailer_name}

#### Example 

please see spiders/net-a-porter.py

##### Create Data Model:


```python
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
```

##### Parse the Page 

```python
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
```

JSON output -> configured to mongodb but can be easily swapped out in middlewares.py...

Scraped from <200 https://www.net-a-porter.com/us/en/product/516570/Ancient_Greek_Sandals/clio-leather-sandals>

```
{"brand": "Ancient Greek Sandals",
 "color": "Heel measures approximately 10mm/ 0.5 inches",
 "description": "Heel measures approximately 10mm/ 0.5 inches Black leather Buckle-fastening slingback strap - - Fits true to size, take your normal size- Only available in full sizes, go up to the nearest whole size if you take a half size- Italian sizing- Narrow at the top of the foot- Heel measures approximately 10mm/ 0.5 inches- Black leather- Buckle-fastening slingback strap",
 "description_legacy": {"bullets": ["Fits true to size, take your normal size",
                                    "Only available in full sizes, go up to the nearest whole size if you take a half size",
                                    "Italian sizing",
                                    "Narrow at the top of the foot",
                                    "Heel measures approximately 10mm/ 0.5 inches",
                                    "Black leather",
                                    "Buckle-fastening slingback strap"],
                        "text": "Heel measures approximately 10mm/ 0.5 inches Black leather Buckle-fastening slingback strap"},
 "gender": "female",
 "google_product_category": "187",
 "image_link": "http://cache.net-a-porter.com/images/products/516570/516570_in_pp.jpg",
 "link": "https://www.net-a-porter.com/us/en/product/516570/Ancient_Greek_Sandals/clio-leather-sandals",
 "price": "185.00",
 "product_id": "516570",
 "store_id": "516570",
 "title": "Ancient Greek Sandals | Clio leather sandals "}
 ```
 
## Built using Scrapy...

For more information including a list of features check the Scrapy homepage at:
https://scrapy.org

## Requirements

* Python 2.7 or Python 3.4+
* Works on Linux, Windows, Mac OSX, BSD

## Install

We highly reccomend you run Google Taxonomy Scraper in a virtualenv

### The quick way:

#### sudo sh ubuntu_install.sh
#### sh mac_install.sh

Note: mac install requires homebrew, and remove mongodb from install script if it's already installed. 

Manual Ubuntu Linux installation: 

```
    sudo apt-get install mongodb
    pip install virtualenv
    virtualenv google-taxonomy-scraper
    cd google-taxonomy-scraper
    git clone git@github.com:duasamericas/google-taxonomy-scraper.git .
    source ./bin/activate 
    pip install scrapy 
```

Manual Mac OSX installation: 

```
    brew install mongodb
    pip install virtualenv
    virtualenv google-taxonomy-scraper
    cd google-taxonomy-scraper
    git clone git@github.com:duasamericas/google-taxonomy-scraper.git .
    source ./bin/activate 
    pip install scrapy 
```

Manual Windows installation: 

```
    Download Ubuntu or buy a mac and follow the above instructions. ;). Just kidding but yeah... 
    Install mongo, virtualenv, create a virtualenv activate it and install scrapy, clone the project and go. 
```
    
Scrapy requires certain libraries to be installed on the system for information on 
which libraries are required and how to install them please see the documentation 
on Scrapy's website...

For more details see the install section in the documentation:
https://doc.scrapy.org/en/latest/intro/install.html


## Commercial Support

support@duasamericasgroup.com
