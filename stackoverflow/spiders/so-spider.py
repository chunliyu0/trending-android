import scrapy
from ..items import StackoverflowItem
# from stackoverflow.stackoverflow.items import StackoverflowItem

class StackoverflowSpider(scrapy.Spider):
    name = "stackoverflow-spider"

    def start_requests(self):
        urls = []
        _url = "https://stackoverflow.com/questions/tagged/android?tab=newest&page={page}&pagesize=15"

        for page in range(1,10000):
            urls.append(_url.format(page=page))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        question_list  = response.xpath('//*[@id="questions"]')

        for question in question_list.xpath('./div'):
            item = StackoverflowItem()
            item['asked_time'] = question.xpath('div[2]/div[3]/div/div[1]/span/@title').extract()
            item['_id'] = question.attrib['id']
            item['question_title'] = question.xpath('div[2]/h3/a/text()').extract()
            item['question_excerpt'] = question.xpath('div[2]/div[1]/text()').extract()
            item['votes'] = question.xpath(
                'div[1]/div[1]/div[1]/div[1]/span/strong/text()').extract()
            item['answers'] = question.xpath(
                'div[1]/div[1]/div[2]/strong/text()').extract()
            item['views'] = question.xpath('div[1]/div[2]/@title').extract()
            item['links'] = question.xpath('div[2]/h3/a/@href').extract()
            yield item

