#! /usr/bin/python
# encoding:utf-8

import tornado.web
import tornado.options
import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options
from sqlalchemy.orm import sessionmaker
import utils.db_utils as db
from handlers import bar_daily as bar_daily_handlers, strategy as strategy_handlers, fut_info as fut_info_handlers
from handlers import indicator as indicator_handlers
import configparser
from utils import spider_runner


define("port", default=9000, help="run on the given port", type=int)

HANDLERS = [
    (r"/api/strategy", strategy_handlers.StrategyHandler),
    (r"/api/strategy_list", strategy_handlers.StrategyListHandler),
    (r"/api/fut_info", fut_info_handlers.FutInfoHandler),
    (r"/api/fut_info_list", fut_info_handlers.FutInfoListHandler),
    (r"/api/bar_daily", bar_daily_handlers.BarDailyHandler),
    (r"/api/bar_daily_list", bar_daily_handlers.BarDailyListHandler),
    (r"/api/indicator", indicator_handlers.IndicatorHandler),
    (r"/api/indicator_list", indicator_handlers.IndicatorListHandler),
]


class Application(tornado.web.Application):
    def __init__(self):
        print("db init")
        engine = db.connent()
        self.DB_Session = sessionmaker(bind=engine)
        db.init_db(engine)
        db.list_tables(db.Base.metadata)
        print("db start")
        cp = configparser.ConfigParser()
        cp.read('./data_spider/scrapy.cfg')
        spider_name = cp.get('deploy', 'project')
        spider_runner.run_inside_spider(spider_name)
        tornado.web.Application.__init__(self, HANDLERS, debug=True)


def run():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    print('server start on port: {}'.format(options.port))
    tornado.ioloop.IOLoop.instance().start()

    # app = tornado.web.Application(
    #     HANDLERS,
    #     debug=True,
    # )
    # http_server = tornado.httpserver.HTTPServer(app)
    # port = 8888
    # http_server.listen(port)
    # print('server start on port: {}'.format(port))
    # tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    run()
