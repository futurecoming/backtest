import json
from utils.imp_untils import imp
from utils.file_utils import img2base64
from handlers.base import BaseHandler
from models.strategy import Strategy
from engine.api import run_backtest


class BacktestResultHandler(BaseHandler):

    def get(self):
        return self.set_status(404)

    def post(self):
        try:
            # 取出客户端提交的json字符串
            json_byte = self.request.body
            json_str = json_byte.decode('utf8')  # 解码，二进制转为字符串
            json_obj = json.loads(json_str)  # 将字符串转为json对象
            symbol_list = json_obj.get('symbol_list')
            init_cash = json_obj.get('init_cash')
            start = json_obj.get('start')
            end = json_obj.get('end')
            strategy_name = json_obj.get('strategy_name')
            strategy_class_name = self.session.query(Strategy.strategy_class_name).filter(
                Strategy.strategy_name == strategy_name).one()
        except KeyError:
            return self.set_status(404)
        config = {
            'symbol_list': symbol_list,
            'init_cash': init_cash,
            'start': start,
            'end': end,
        }
        clszz = imp('engine.strategies.ma_cross', strategy_class_name[0])
        order_list, stats_ret = run_backtest(clszz, config)
        resp = {'status': True, 'data': {'order_list': order_list, 'stats_ret': stats_ret,
                                         'cumulative_return': 'http://localhost:9000/static/cumulative_return.png'}}
        resp = json.dumps(resp, ensure_ascii=False)
        self.finish(resp)


if __name__ == '__main__':
    # from utils.imp_untils import imp
    # config = {
    #     'symbol_list': ['AU', 'AL', 'CU'],
    #     'init_cash': 100000000.0,
    #     'start': '2015-04-08',
    #     'end': '2017-10-27',
    # }
    # clszz = imp('engine.strategies.ma_cross', 'MovingAverageCrossStrategy')
    # print(clszz)
    # run_backtest(clszz, config)
    pass
