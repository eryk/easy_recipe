import scrapy

from easy_recipe.items import RecipeItem


class MeishiChinaSpider(scrapy.Spider):
    name = 'meishichina'
    allowed_domains = ['meishichina.com']
    start_urls = ['https://home.meishichina.com/show-top-type-recipe-page-1.html']
    nexted = False

    def parse(self, response):
        recipe_list = response.css('.ui_newlist_1 ul .pic').xpath('a')
        print('recipe_list:',recipe_list)
        for recipe_detail in recipe_list:
            recipe_url = recipe_detail.xpath('@href').extract_first()
            print("recipe_url:", recipe_url)
            yield scrapy.Request(recipe_url, callback=self.parse_content)

        next_page = response.css('.ui-page-inner a')[-1]
        if next_page:
            next_page_url = next_page.xpath('@href').extract_first()
            print('next_page:', next_page_url)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_content(self, response):
        item = RecipeItem()
        item['title'] = response.css('#recipe_title::text').extract_first()
        if item['title'] is None:
            return
        item['url'] = response.url
        item['pic'] = response.css('.J_photo img').xpath('@src').extract_first()
        item['ingredient'] = response.css('.recipDetail .category_s1 b::text').extract()
        yield item
