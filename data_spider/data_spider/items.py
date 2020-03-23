# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class FutInfoItem(Item):
    code = Field()
    exchange = Field()
    name = Field()
    create_time = Field()
    update_time = Field()
    pass


class BarDailyItem(Item):
    trade_date = Field()
    pre_close = Field()
    open = Field()
    high = Field()
    close = Field()
    low = Field()
    change = Field()
    vol = Field()
    amount = Field()
    oi = Field()
    oi_chg = Field()
    create_time = Field()
    update_time = Field()
    pass
