# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EasyRecipeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class RecipeItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    pic = scrapy.Field()
    ingredient = scrapy.Field()


class MaoyanreyingItem(scrapy.Item):
    index = scrapy.Field()
    title = scrapy.Field()
    star = scrapy.Field()
    releaseTime = scrapy.Field()
    score = scrapy.Field()
