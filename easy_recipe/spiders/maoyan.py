import scrapy

from easy_recipe.items import MaoyanreyingItem


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://www.maoyan.com/board/7/']

    def parse(self, response):
        dl = response.css('.board-wrapper dd')
        for dd in dl:
            item = MaoyanreyingItem()
            item['index'] = dd.css('.board-index::text').extract_first()
            item['title'] = dd.css('.name a::text').extract_first()
            item['star'] = dd.css('.star::text').extract_first()
            item['releaseTime'] = dd.css('.releasetime::text').extract_first()
            item['score'] = dd.css('.integer::text').extract_first()
            yield item
