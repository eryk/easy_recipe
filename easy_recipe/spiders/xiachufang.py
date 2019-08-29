from time import sleep
from urllib.parse import urljoin

import scrapy

from easy_recipe.items import RecipeItem


class XiachufangSpider(scrapy.Spider):
    name = 'xiachufang'
    allowed_domains = ['xiachufang.com']
    start_urls = [
        # 'http://www.xiachufang.com/category/40076/?page=1',
        # 'http://www.xiachufang.com/category/40077/?page=1',
        'http://www.xiachufang.com/category/40078/?page=1',
        # 'http://www.xiachufang.com/category/40078/?page=1',
        # 'http://www.xiachufang.com/category/51848/?page=1',
        # 'http://www.xiachufang.com/category/52354/?page=1',
        # 'http://www.xiachufang.com/category/51743/?page=1',
        # 'http://www.xiachufang.com/category/52351/?page=1',
        # 'http://www.xiachufang.com/category/51940/?page=1'
    ]
    SITE_URL = 'http://www.xiachufang.com'

    def parse(self, response):
        recipe_list = response.css('.normal-recipe-list .recipe').xpath('a')
        for recipe_detail in recipe_list:
            recipe_url = recipe_detail.xpath('@href').extract_first()
            print(urljoin(self.SITE_URL, recipe_url))
            yield scrapy.Request(urljoin(self.SITE_URL, recipe_url), callback=self.parse_content)

        next_page = response.css('.pager .next')
        if next_page:
            next_page_url = next_page.xpath('@href').extract_first()
            print('next_page:', urljoin(self.SITE_URL, next_page_url))
            sleep(3)
            yield scrapy.Request(urljoin(self.SITE_URL, next_page_url), callback=self.parse)

    def parse_content(self, response):
        item = RecipeItem()
        item['title'] = response.css('.page-title::text').extract_first()
        if item['title'] is None:
            return
        item['title'] = str(item['title']).replace("\n", '').replace(' ', '')
        item['url'] = response.url
        item['pic'] = response.css('.recipe-show img').xpath('@src').extract_first()
        ingredient = list()
        ingredient.extend(list(map(lambda item: str(item).replace("\n", '').replace(' ', ''),
                                      response.css('.ings .name::text').extract())))
        ingredient.extend(list(map(lambda item: str(item).replace("\n", '').replace(' ', ''),
                     response.css('.ings .name a::text').extract())))
        ingredient = list(filter(lambda item: item is not '', ingredient))
        item['ingredient'] = ingredient
        yield item
