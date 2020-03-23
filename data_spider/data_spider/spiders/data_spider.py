import json
import datetime
import scrapy
from enum import Enum
from scrapy.utils.project import get_project_settings
from data_spider.items import FutInfoItem, BarDailyItem
# import sys
# sys.path.append(r"F:\py\backtest\utils")
# print(sys.path)
from utils import time_utils

settings = get_project_settings()


class FutName(Enum):
    SS = '不锈钢'
    AL = '沪铝'
    CU = '沪铜'
    ZN = '沪锌'
    AG = '白银'
    RB = '螺纹钢'
    SN = '沪锡'
    NI = '沪镍'
    WR = '线材'
    FU = '燃油'
    AU = '黄金'
    PB = '沪铅'
    RU = '橡胶'
    HC = '热轧卷板'
    BU = '沥青'
    SP = '纸浆'


class DataSpider(scrapy.spiders.Spider):
    name = "data_spider"
    allowed_domains = [settings.get('TUSHARE_URL')]

    def start_requests(self):
        url = 'http://' + settings.get('TUSHARE_URL')
        # payload = {
        #         'api_name': settings.get('TUSHARE_API'),
        #         'token': settings.get('TUSHARE_TOKEN'),
        #         'params': {
        #             'trade_date': '20181113',
        #             'exchange': 'SHFE'
        #         }
        #     }
        # yield scrapy.Request(url=url, method='POST', callback=self.parse_data, body=json.dumps(payload))
        begin = datetime.date(2018, 1, 1)
        end = datetime.date(2020, 1, 1)
        for i in range((end - begin).days + 1):
            day = begin + datetime.timedelta(days=i)
            trade_date = str(day).replace('-', '')
            payload = {
                'api_name': settings.get('TUSHARE_API'),
                'token': settings.get('TUSHARE_TOKEN'),
                'params': {
                    'exchange': 'SHFE',
                    'trade_date': trade_date
                }
            }
            time_utils.sleep(1)
            yield scrapy.Request(url=url, method='POST', callback=self.parse_data, body=json.dumps(payload))

    def parse_data(self, response):
        # print(response)
        content = response.text
        data = json.loads(content)['data']['items']
        # print(data)
        for i in range(len(data)):
            fut_info_item = FutInfoItem()
            bar_daily_item = BarDailyItem()
            fut_code = str(data[i][0])
            # 过滤获取主力合约
            for name, member in FutName.__members__.items():
                if fut_code == name:
                    # 填充合约信息模型
                    fut_info_item['code'] = fut_code
                    fut_info_item['exchange'] = str(data[i][0].split(".")[1])
                    fut_info_item['name'] = member.value
                    # 填充bar模型
                    bar_daily_item['trade_date'] = str(data[i][0].split(".")[0])
                    bar_daily_item['pre_close'] = str(data[i][2])
                    bar_daily_item['open'] = str(data[i][4])
                    bar_daily_item['high'] = str(data[i][5])
                    bar_daily_item['low'] = str(data[i][6])
                    bar_daily_item['close'] = str(data[i][7])
                    bar_daily_item['change'] = str(data[i][9])
                    bar_daily_item['vol'] = str(data[i][11])
                    bar_daily_item['amount'] = str(data[i][12])
                    bar_daily_item['oi'] = str(data[i][13])
                    bar_daily_item['oi_chg'] = str(data[i][14])
                    fut_info_item['create_time'] = time_utils.get_format_datetime()
                    fut_info_item['update_time'] = time_utils.get_format_datetime()
                    bar_daily_item['create_time'] = time_utils.get_format_datetime()
                    bar_daily_item['update_time'] = time_utils.get_format_datetime()
                    yield fut_info_item, bar_daily_item
