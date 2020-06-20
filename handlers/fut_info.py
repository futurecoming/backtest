from models.fut_info import FutInfo
from handlers.base import BaseHandler


class FutInfoHandler(BaseHandler):

    def get(self):
        try:
            fut_id = self.get_query_argument('fut_id')
            fut_info = self.session.query(FutInfo).filter(FutInfo.id == fut_id).one()
        except KeyError:
            return self.set_status(404)
        fut_info = FutInfo.to_dict(fut_info)
        resp = {'status': True, 'data': fut_info}
        self.finish(resp)


class FutInfoListHandler(BaseHandler):

    def get(self):
        try:
            fut_info_list = self.session.query(FutInfo).all()
        except KeyError:
            return self.set_status(404)
        fut_info_list = FutInfo.to_json(fut_info_list)
        resp = {'status': True, 'data': fut_info_list}
        self.finish(resp)
