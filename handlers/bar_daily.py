import json
from models.bar_daily import BarDaily
from handlers.base import BaseHandler


class BarDailyListHandler(BaseHandler):

    def post(self):
        try:
            json_byte = self.request.body
            json_str = json_byte.decode('utf8')
            json_obj = json.loads(json_str)
            symbol = json_obj.get('symbol')
            start_date = json_obj.get('start_date')
            end_date = json_obj.get('end_date')
            ret = self.session.query(BarDaily).filter(BarDaily.fut_code == symbol,
                                                      BarDaily.trade_date.between(start_date,
                                                                                  end_date)).order_by("trade_date").all()
            bars = BarDaily.to_json(ret)
            bar_daily_list = []
            for bar in bars:
                _bar = []
                for k, v in bar.items():
                    if k == 'trade_date':
                        _bar.insert(0, v.split(' ')[0])
                    if k == 'open':
                        _bar.insert(1, float(v))
                    if k == 'close':
                        _bar.insert(2, float(v))
                    if k == 'low':
                        _bar.insert(3, float(v))
                    if k == 'high':
                        _bar.insert(4, float(v))
                bar_daily_list.append(_bar)
        except KeyError:
            return self.set_status(404)
        resp = {'status': True, 'data': bar_daily_list}
        resp = json.dumps(resp, ensure_ascii=False)
        self.finish(resp)
