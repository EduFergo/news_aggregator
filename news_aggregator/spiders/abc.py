# You have to create three separate spider files in the spiders/ folder (e.g., bbc.py, elpais.py, reuters.py).
# Requirements for each spider:
# Identify the correct CSS or XPath selectors for that specific site.
# Create a spider with only CSS selectors at least
# Create a spider with only Xpath selector at least
# The third spider is on your own
# Extract at least three characteristics (e.g., Title, Date, Author, ...).
# Clean the data: Remove extra whitespace, newlines (\n), or "By" prefixes from author names.
# Add always a "source" field with each register to identify the news page

import scrapy
from ..items import NewsAggregatorItem

class AbcSpider(scrapy.Spider):
    name = "abc"
    allowed_domains = ["abc.es"]
    start_urls = ["https://www.abc.es/"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seen_urls = set()

    def parse(self, response):
        articles = response.css('article')
        for idx, article in enumerate(articles):
            link = article.css("h2 a::attr(href)").get()
            if link and link not in self.start_urls:
                self.seen_urls.add(link)
                yield response.follow(link, callback = self.parse_article, cb_kwargs={'position': idx + 1})

    def parse_article(self, response, position):
        item = NewsAggregatorItem()
        item['position'] = position
        item['title'] = response.css('h1::text').get(default='').strip()
        item['date'] = response.css('section.voc-author time::attr(datetime)').get()
        author = response.css('section.voc-author p.voc-author__name a::text').get(default='')
        item['author'] = author.strip() if author else None
        item['source'] = "ABC"
        item['url'] = response.url

        yield item

