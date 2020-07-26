# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UbereatsItem(scrapy.Item):
    # define the fields for your item here like:
    restaurant_name = scrapy.Field()
    food_type = scrapy.Field()
    delivery_time = scrapy.Field()
    rating = scrapy.Field()
    address = scrapy.Field()
    popular_food = scrapy.Field()
    menu = scrapy.Field()
    