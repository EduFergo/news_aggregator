import scrapy
from ..items import NewsAggregatorItem

class ElPaisSpider(scrapy.Spider):
    name = "elpais"
    allowed_domains = ["elpais.com"]
    start_urls = ["https://elpais.com/"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seen_urls = set()

    def parse(self, response):
        articles = response.xpath('//article[not(ancestor::section[contains(@data-dtm-region, "pasatiempos")])]')
        for idx, article in enumerate(articles):
            link = article.xpath('.//h2/a/@href | .//h3/a/@href').get()
            if link and link not in self.start_urls and link not in self.seen_urls:
                self.seen_urls.add(link)
                yield response.follow(link, callback=self.parse_article, cb_kwargs={'position': idx + 1})

    def parse_article(self, response, position):
        item = NewsAggregatorItem()
        item['position'] = position
        item['title'] = response.xpath('//h1[@class="a_t"]/text()').get(default='').strip()
        author = response.xpath('//div[@class="a_md_a"]/a/text()').get(default='')
        item['author'] = author.strip() if author else None
        item['date'] = response.xpath('//time/@datetime').get()
        item['source'] = "El País"

        yield item