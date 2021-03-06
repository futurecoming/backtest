from models.base import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String


class FutInfo(BaseModel):  # 继承生成的orm基类
    __tablename__ = "fut_info"  # 表名
    code = Column(String(8), unique=True)  # 合约代码
    exchange = Column(String(8))  # 交易所代码
    name = Column(String(16), unique=True)  # 中文简称
    # 在父表类中通过 relationship() 方法来引用子表的类集合
    bar_daily = relationship("BarDaily", backref="fut_info")
