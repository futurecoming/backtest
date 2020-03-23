# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# from scrapy.utils.project import get_project_settings
# settings = get_project_settings()
from sqlalchemy.orm import sessionmaker

import utils.db_utils as db
from models import *

FutInfo = fut_info.FutInfo
BarDaily = bar_daily.BarDaily


class DataSpiderPipeline(object):
    def __init__(self):
        engine = db.connent()
        DB_Session = sessionmaker(bind=engine)
        db.init_db(engine)
        db.list_tables(db.Base.metadata)
        self.db_session = DB_Session()

    async def process_item(self, fut_info_item, bar_daily_item):
        code = fut_info_item['code']
        exchange = fut_info_item['exchange']
        name = fut_info_item['name']
        f_create_time = fut_info_item['create_time']
        f_update_time = fut_info_item['update_time']
        _fut_info = FutInfo(id=None, code=code, exchange=exchange, name=name, create_time=f_create_time,
                            update_time=f_update_time)
        self.db_session.add(_fut_info)
        await self.db_session.commit()
        f_id = await self.db_session.query(FutInfo.id).order_by(FutInfo.create_time).first()
        trade_date = bar_daily_item['trade_date']
        pre_close = bar_daily_item['pre_close']
        open = bar_daily_item['open']
        high = bar_daily_item['high']
        low = bar_daily_item['low']
        close = bar_daily_item['close']
        change = bar_daily_item['change']
        vol = bar_daily_item['vol']
        amount = bar_daily_item['amount']
        oi = bar_daily_item['oi']
        oi_chg = bar_daily_item['oi_chg']
        b_create_time = bar_daily_item['create_time']
        b_update_time = bar_daily_item['update_time']
        _bar_daily = BarDaily(id=None, fut_id=f_id, trade_date=trade_date, pre_close=pre_close, open=open, high=high,
                              low=low, close=close, change=change, vol=vol, amount=amount,
                              oi=oi, oi_chg=oi_chg, create_time=b_create_time, update_time=b_update_time)
        self.db_session.add(_bar_daily)
        await self.db_session.commit()

        return fut_info_item, bar_daily_item
