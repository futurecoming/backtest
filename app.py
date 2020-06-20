#! /usr/bin/python
# encoding:utf-8
import os

import tornado.web
import tornado.options
import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options
from sqlalchemy.orm import sessionmaker
import utils.db_utils as db
from handlers import bar_daily as bar_daily_handlers, strategy as strategy_handlers, fut_info as fut_info_handlers
from handlers import backtest_result as backtest_handlers

define("port", default=9000, help="run on the given port", type=int)

HANDLERS = [
    (r"/api/strategy", strategy_handlers.StrategyHandler),
    (r"/api/strategy_list", strategy_handlers.StrategyListHandler),
    (r"/api/fut_info", fut_info_handlers.FutInfoHandler),
    (r"/api/fut_info_list", fut_info_handlers.FutInfoListHandler),
    (r"/api/bar_daily_list", bar_daily_handlers.BarDailyListHandler),
    (r"/api/backtest", backtest_handlers.BacktestResultHandler),
]


class Application(tornado.web.Application):
    def __init__(self):
        setting = dict(
            static_path=os.path.join(os.path.dirname(__file__), "output"),
        )
        print("db init")
        engine = db.connent()
        self.DB_Session = sessionmaker(bind=engine)
        # db.drop_db(engine)
        db.init_db(engine)
        # db.list_tables(db.Base.metadata)
        print("db start")
        tornado.web.Application.__init__(self, HANDLERS, debug=True, **setting)


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
