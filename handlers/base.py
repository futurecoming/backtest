from tornado.web import RequestHandler
import tornado.util


class BaseHandler(RequestHandler):

    def initialize(self):
        self.session = self.application.DB_Session()

    def on_finish(self):
        self.session.close()

    @staticmethod
    def row_to_obj(row, cur):
        """Convert data_spider db row to an object supporting dict and attribute access."""
        obj = tornado.util.ObjectDict()
        for val, desc in zip(row, cur.description):
            obj[desc.name] = val
        return obj
