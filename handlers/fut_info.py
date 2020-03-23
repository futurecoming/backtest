from tornado.escape import json_encode
from models.fut_info import FutInfo
from handlers.base import BaseHandler


class FutInfoHandler(BaseHandler):

    def get(self, f_id):
        try:
            fut_info = self.session.query(FutInfo).filter(FutInfo.id == f_id).one()
        except KeyError:
            return self.set_status(404)
        print(fut_info)
        self.write(json_encode(fut_info))


class FutInfoListHandler(BaseHandler):

    def get(self):
        try:
            fut_info_list = self.session.query(FutInfo).all()
        except KeyError:
            return self.set_status(404)
        print(fut_info_list)
        self.write(json_encode(fut_info_list))
