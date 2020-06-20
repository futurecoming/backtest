import json
import re
from utils import file_utils as f
from models.strategy import Strategy
from handlers.base import BaseHandler
from utils import time_utils


class StrategyHandler(BaseHandler):

    def get(self):
        try:
            s_id = self.get_query_argument('strategy_id')
            strategy = self.session.query(Strategy).filter(Strategy.id == s_id).one()
        except KeyError:
            return self.set_status(404)
        strategy = Strategy.to_dict(strategy)
        strategy['code'] = f.read_file(strategy['code_location'])
        print(strategy['code'])
        resp = {'status': True, 'data': strategy}
        self.finish(resp)

    def post(self):
        try:
            json_byte = self.request.body
            json_str = json_byte.decode('utf8')
            json_obj = json.loads(json_str)
            strategy_name = json_obj.get('strategy_name')
            code = json_obj.get('code')
            strategy_class_name = re.findall(".*class (.*)\(Strategy.*", code)[0]
            code_location = f.write2file(strategy_name, code)
            _time = time_utils.get_format_datetime()
            strategy = Strategy(strategy_name=strategy_name, strategy_class_name=strategy_class_name,
                                code_location=code_location, create_time=_time,
                                update_time=_time)
            self.session.add(strategy)
            self.session.commit()
        except KeyError:
            return self.set_status(500)
        else:
            resp = {'status': True, 'msg': 'create ' + strategy_name + ' strategy success'}
            self.finish(resp)

    def put(self):
        try:
            json_byte = self.request.body
            json_str = json_byte.decode('utf8')
            json_obj = json.loads(json_str)
            s_id = json_obj.get('strategy_id')
            _update = {}
            strategy_name = json_obj.get('strategy_name')
            code = json_obj.get('code')
            strategy_class_name = re.findall(".*class (.*)\(Strategy.*", code)[0]
            code_location = f.write2file(strategy_name, code)
            _update["strategy_name"] = strategy_name
            _update["strategy_class_name"] = strategy_class_name
            _update["code_location"] = code_location
            _time = time_utils.get_format_datetime()
            self.session.query(Strategy).filter(Strategy.id == s_id).update(_update)
            self.session.commit()
        except KeyError:
            return self.set_status(500)
        else:
            resp = {'status': True, 'msg': 'update ' + json_obj.get('strategy_name') + ' strategy success'}
            self.finish(resp)

    def delete(self):
        try:
            s_id = self.get_query_argument('strategy_id')
            self.session.query(Strategy).filter(Strategy.id == s_id).delete()
            self.session.commit()
        except KeyError:
            return self.set_status(500)
        else:
            resp = {'status': True, 'msg': 'delete success'}
            self.finish(resp)


class StrategyListHandler(BaseHandler):

    def get(self):
        try:
            strategy_list = self.session.query(Strategy).all()
        except KeyError:
            return self.set_status(404)
        strategy_list = Strategy.to_json(strategy_list)
        resp = {'status': True, 'data': strategy_list}
        self.finish(resp)
