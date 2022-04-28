import scrapy
from scrapy.http import Request
from war2022_team15.items import War2022Team15Item
import json
import hashlib

class Rbc_articlesSpider(scrapy.Spider):
    name = 'rbc_articles'
    allowed_domains = ['rbc.ru']
    start_urls = []

    def start_requests(self):
        # Open the JSON file which contains article links
        data=[]
        with open('./rbc.json') as json_file:
            data = json.load(json_file)

        for link_url in data:
            print('URL: ' + link_url['article_url'])
            # Request to get the HTML content
            request = Request(link_url['article_url'],
                              cookies={'store_language': 'ru'},
                              callback=self.parse)
            yield request

    def parse(self, response):
        item = War2022Team15Item()

        news_body = ""
        # Extracts the news_title and stores in scrapy item
        item['article_link'] = response.url
        item['article_uuid'] = hashlib.sha256(str(response.url).encode('utf-8')).hexdigest()
        item['article_id'] = response.url.split("/")[-1]
        item['article_datetime'] = response.xpath("//span[@itemprop='datePublished']/text()").extract_first()
        item['article_title'] = response.xpath("//h1[@itemprop='headline']/text()").extract_first().replace('\n', '').replace('                    ','')
        temp1 = response.xpath("((//div[@class='article__text article__text_free' and @itemprop ='articleBody'])[1])/p/text()").extract()
        temp2=""
        for line in temp1:
            temp2+=line.replace('\xa0',' ').replace('\n','')
        item['article_text'] = temp2

        yield (item)
