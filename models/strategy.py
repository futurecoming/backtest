from models.base import BaseModel
from sqlalchemy import Column, String


class Strategy(BaseModel):  # 继承生成的orm基类
    __tablename__ = "strategy"  # 表名
    strategy_name = Column(String(16))  # 策略名称
    code_location = Column(String(32))  # 策略代码位置

    def __init__(self, strategy_name, code_location, id, create_time, update_time):
        super().__init__(id, create_time, update_time)
        self.strategy_name = strategy_name
        self.code_location = code_location

    def __repr__(self):
        return "<Strategy('%s','%s')>" % (self.strategy_name, self.code_location)
