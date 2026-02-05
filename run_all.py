from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from news_aggregator.spiders.abc import AbcSpider
from news_aggregator.spiders.elpais import ElPaisSpider
from news_aggregator.spiders.lvdg import LvdgSpider


if __name__ == "__main__":
    settings = get_project_settings()

    settings.update({
        'FEEDS': {
            'all_news.json': {
                'format': 'json',
                'encoding': 'utf8',
                'store_empty': False,
                'indent': 2,
                'overwrite': False
            }
        }
    })

    process = CrawlerProcess(settings)

    process.crawl(ElPaisSpider)
    process.crawl(LvdgSpider)
    process.crawl(AbcSpider)

    process.start()