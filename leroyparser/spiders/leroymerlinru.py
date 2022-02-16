import scrapy
from scrapy.http import HtmlResponse
from leroyparser.items import LeroyparserItem


class LeroymerlinruSpider(scrapy.Spider):
    name = 'leroymerlinru'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://leroymerlin.ru/catalogue/{kwargs.get("search")}/']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[contains(@aria-label, "Следующая страница")]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath('//a[@data-qa="product-name"]')

        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        link = response.url
        name = response.xpath('//h1/text()').get()
        price = response.xpath('//span[@slot="price"]/text()').get()
        images = response.xpath('//uc-pdp-media-carousel//source[contains(@media, "min-width: 1024px")]/@data-origin').getall()
        yield LeroyparserItem(name=name, link=link, price=price, images=images)
