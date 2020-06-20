from models.base import BaseModel
from sqlalchemy import Column, String


class Strategy(BaseModel):  # 继承生成的orm基类
    __tablename__ = "strategy"  # 表名
    strategy_name = Column(String(32))  # 策略名称
    strategy_class_name = Column(String(32))  # 策略类名
    code_location = Column(String(64))  # 策略文件位置
