import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class QuotesSpider(CrawlSpider):
    name = 'quotes'
    allowed_domains = ['www.brainyquote.com']

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(
            url='http://www.brainyquote.com/topics/',
            headers={
                'User-Agent': self.user_agent
            }
        )

    rules = (
        Rule(
            LinkExtractor(restrict_xpaths="//a[contains(@class, 'topicIndexChicklet')]"),
            callback='parse_item',
            follow=True,
            process_request='set_user_agent'
        ),
    )

    def set_user_agent(self, request):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        yield scrapy.Request(
            response.url,
            callback=self.parse_quotes,
            dont_filter=True,
            headers={
                'User-Agent': self.user_agent
            }
        )

    def parse_quotes(self, response):
        for quote in response.xpath("//a[@title='view quote']/@href"):
            yield response.follow(
                quote,
                callback=self.parse_quote_detail,
                dont_filter=True,
                headers={
                    'User-Agent': self.user_agent
                }
            )

    def parse_quote_detail(self, response):
        biography = {}
        for bio in response.xpath("//div[contains(@class, 'autoBioDet')]/div/div/div/div/div"):
            key = bio.xpath("./text()").get()
            if key:
                key = key.strip('\n')
            value = bio.xpath(".//a/text()").get()
            if value:
                value = value.strip('\n')
            if 'Born' in key or 'Died' in key:
                if value:
                    value += bio.xpath("./text()[2]").get()
                else:
                    value = bio.xpath("./text()[2]").get()
                if value:
                    value = value.strip('\n')
            biography[key] = value

        yield {
            'url': response.url,
            'quote_text': response.xpath("(//div[@class='quoteContent']/div)[last()]/p/text()").get(),
            'authors': response.xpath("(//div[@class='quoteContent']/div)[last()]/p[last()]/a/text()").get(),
            'biography': biography,
            'related_authors': response.xpath("//div[contains(@class, 'autoBioDet')]/div/div[3]/div/div/a/text()").getall(),
            'topics': response.xpath("//div[contains(@class, 'autoBioDet')]/div/div[4]/div/div/a/text()").getall()
        }