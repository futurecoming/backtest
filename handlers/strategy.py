from tornado.escape import json_encode
from models.strategy import Strategy
from handlers.base import BaseHandler
from utils import time_utils


class StrategyHandler(BaseHandler):

    def get(self, s_id):
        try:
            strategy = self.session.query(Strategy).filter(Strategy.id == s_id).one()
        except KeyError:
            return self.set_status(404)
        print(strategy)
        self.write(json_encode(strategy))
        # self.write(json_encode(strategies))
        # self.write(str(strategies))

    def post(self):
        strategy_name = self.get_argument('strategy_name')
        code_location = self.get_argument('code_location')
        _time = time_utils.get_format_datetime()
        strategy = Strategy(strategy_name=strategy_name, code_location=code_location, create_time=_time,
                            update_time=_time)
        self.session.add(strategy)
        self.session.commit()
        resp = {'status': True, 'msg': 'create' + str(strategy) + 'success'}
        self.write(json_encode(resp))

    def put(self, s_id):
        strategy_name = self.get_argument('strategy_name')
        code_location = self.get_argument('code_location')
        _time = time_utils.get_format_datetime()
        res = self.session.query(Strategy).filter(Strategy.id == s_id).update(strategy_name=strategy_name,
                                                                              code_location=code_location,
                                                                              update_time=_time)
        self.session.commit()
        resp = {'status': True, 'msg': str(res)}
        self.write(json_encode(resp))

    def delete(self, s_id):
        self.session.query(Strategy).filter(Strategy.id == s_id).delete()
        resp = {'status': True, 'msg': 'delete success'}
        self.write(json_encode(resp))


class StrategyListHandler(BaseHandler):

    def get(self):
        try:
            strategy_list = self.session.query(Strategy).all()
        except KeyError:
            return self.set_status(404)
        print(strategy_list)
        self.write(json_encode(strategy_list))
