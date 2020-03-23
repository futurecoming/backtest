# encoding: utf-8
from twisted.internet import reactor
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging


def run_single_spider(spider):
    """Running spiders outside projects
    只调用spider，不会进入pipeline"""
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(spider)
    process.start()  # the script will block here until the crawling is finished


def run_inside_spider(spider):
    """会启用pipeline"""
    from scrapy.crawler import CrawlerProcess
    process = CrawlerProcess(get_project_settings())
    process.crawl(spider)  # scrapy项目中spider的name值
    process.start()


def spider_closing():
    print('spider close')
    reactor.stop()


def run_crawler_runner():
    """如果你的应用程序使用了twisted，建议使用crawlerrunner 而不是crawlerprocess
    Note that you will also have to shutdown the Twisted reactor yourself after the spider is finished.
    This can be achieved by adding callbacks to the deferred returned by the CrawlerRunner.crawl method.
    """
    from scrapy.crawler import CrawlerRunner
    runner = CrawlerRunner(get_project_settings())

    # 'spidername' is the name of one of the spiders of the project.
    d = runner.crawl('spidername')

    # stop reactor when spider closes
    # d.addBoth(lambda _: reactor.stop())
    d.addBoth(spider_closing)  # 等价写法

    reactor.run()  # the script will block here until the crawling is finished


def run_multiple_spider(spider1, spider2):
    from scrapy.crawler import CrawlerProcess
    process = CrawlerProcess()
    for s in [spider1, spider2]:
        process.crawl(s)
    process.start()


def run_multiple_spider_with_crawler_runner(spider1, spider2):
    """using CrawlerRunner"""
    configure_logging()
    runner = CrawlerRunner()
    for s in [spider1, spider2]:
        runner.crawl(s)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()  # the script will block here until all crawling jobs are finished


def run_multiple_spider_with_chaining():
    """通过链接(chaining) deferred来线性运行spider"""
    from twisted.internet import reactor, defer
    from scrapy.crawler import CrawlerRunner
    from scrapy.utils.log import configure_logging
    configure_logging()
    runner = CrawlerRunner()

    @defer.inlineCallbacks
    def crawl(spider1, spider2):
        for s in [spider1, spider2]:
            yield runner.crawl(s)
        reactor.stop()

    crawl()
    reactor.run()  # the script will block here until the last crawl call is finished


if __name__ == '__main__':
    run_inside_spider('')
