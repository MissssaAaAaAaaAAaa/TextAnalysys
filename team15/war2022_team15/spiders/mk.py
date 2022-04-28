import scrapy
from scrapy.http import Request
from war2022_team15.items import War2022Team15Item


class MKSpider(scrapy.Spider):
    name = 'mk'
    allowed_domains = ['mk.ru']
    start_urls = ['https://www.mk.ru/economics/']
    handle_httpstatus_list = [403]

    def start_requests(self):
        for link_url in self.start_urls:
            print(link_url)
            # Request to get the HTML content
            request = Request(link_url, cookies={'store_language': 'ru'},
                              callback=self.parse)
            yield request

    def parse(self, response):
        # print("\n")
        # print("HTTP STATUS: " + str(response.status))
        # print(response.xpath("//h2/a/text()").get())
        # print("\n")
        item = War2022Team15Item()
        # Gets HTML content where the article links are stored
        content = response.xpath("//div[@class='listing-item__content']/a")
        # Loops through the each and every article link in HTML 'content'
        for article_link in content:
            # Extracts the href info of the link to store in scrapy item
            item['article_url'] = article_link.xpath('.//@href').extract_first()
            print(item['article_url'])
            yield (item)


