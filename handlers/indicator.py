from tornado.escape import json_encode
from models.indicator import Indicator
from handlers.base import BaseHandler


class IndicatorHandler(BaseHandler):

    def get(self, i_id):
        try:
            indicator = self.session.query(Indicator).filter(Indicator.id == i_id).one()
        except KeyError:
            return self.set_status(404)
        print(indicator)
        self.write(json_encode(indicator))

    # def post(self):
    #     strategy_name = self.get_argument('strategy_name')
    #     code_location = self.get_argument('code_location')
    #     _time = time_utils.get_format_datetime()
    #     strategy = Strategy(strategy_name=strategy_name, code_location=code_location, create_time=_time,
    #                         update_time=_time)
    #     self.session.add(strategy)
    #     self.session.commit()
    #     resp = {'status': True, 'msg': 'create' + str(strategy) + 'success'}
    #     self.write(json_encode(resp))
    #
    # def put(self, s_id):
    #     strategy_name = self.get_argument('strategy_name')
    #     code_location = self.get_argument('code_location')
    #     _time = time_utils.get_format_datetime()
    #     res = self.session.query(Strategy).filter(Strategy.id == s_id).update(strategy_name=strategy_name,
    #                                                                           code_location=code_location,
    #                                                                           update_time=_time)
    #     self.session.commit()
    #     resp = {'status': True, 'msg': str(res)}
    #     self.write(json_encode(resp))
    #
    # def delete(self, s_id):
    #     self.session.query(Strategy).filter(Strategy.id == s_id).delete()
    #     resp = {'status': True, 'msg': 'delete success'}
    #     self.write(json_encode(resp))


class IndicatorListHandler(BaseHandler):

    def get(self):
        try:
            indicator_list = self.session.query(Indicator).all()
        except KeyError:
            return self.set_status(404)
        print(indicator_list)
        self.write(json_encode(indicator_list))
