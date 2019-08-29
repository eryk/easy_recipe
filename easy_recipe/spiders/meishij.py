import scrapy

from easy_recipe.items import RecipeItem


class MeishijSpider(scrapy.Spider):
    name = 'meishij'
    allowed_domains = ['meishij.net']
    start_urls = ['https://www.meishij.net/chufang/diy/?&page=1']

    def parse(self, response):
        recipe_list = response.css('.listtyle1_list .listtyle1').xpath('a')
        for recipe_detail in recipe_list:
            recipe_url = recipe_detail.xpath('@href').extract_first()
            yield scrapy.Request(recipe_url, callback=self.parse_content)

        next_page = response.css('.listtyle1_page_w .next')
        if next_page:
            next_page_url = next_page.xpath('@href').extract_first()
            print('next_page:', next_page_url)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_content(self, response):
        item = RecipeItem()
        item['title'] = response.css('#tongji_title::text').extract_first()
        if item['title'] is None:
            return
        item['url'] = response.url
        item['pic'] = response.css('.cp_headerimg_w img').xpath('@src').extract_first()
        item['ingredient'] = response.css('.materials_box a::text').extract()
        yield item
