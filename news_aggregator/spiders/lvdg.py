import scrapy
from ..items import NewsAggregatorItem

class LvdgSpider(scrapy.Spider):
    name = "lvdg"
    allowed_domains = ["lavozdegalicia.es"]
    start_urls = ["https://www.lavozdegalicia.es/"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seen_urls = set()

    def parse(self, response):
        articles = response.css('article')
        for idx, article in enumerate(articles):
            link = article.css("h4 a::attr(href)").get()
            if "/noticia/listisimas/" in link:
                continue
            if link and '/noticia/' in link and link not in self.seen_urls:
                self.seen_urls.add(link)
                yield response.follow(link, callback = self.parse_article, cb_kwargs={'position': idx + 1})

    def parse_article(self, response, position):
        item = NewsAggregatorItem()
        item['position'] = position
        title_clean = response.css('h1.headline span::text, h1.headline::text').getall()
        item['title'] = ' '.join([t.strip() for t in title_clean]).replace('\xa0', ' ').strip()
        item['date'] = response.css('div.date span.sz-t-xs strong::text').get()
        authors = response.css('span.author a::text').getall()
        item['author'] = ', '.join([author.strip() for author in authors]) if authors else None
        item['source'] = "La Voz de Galicia"
        item['url'] = response.url

        #Las noticias Spam que continen el formato noticia en la url tienen en común que no tinene ni título, ni autor, ni fecha.
        #Por lo tanto, si no se encuentra ninguno de estos campos, se descarta la noticia.
        if not any([item['title'], item['author'], item['date']]):
                return
        yield item