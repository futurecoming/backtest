from utils.db_utils import Base
# 导入字段类型
from sqlalchemy import Integer, DateTime
from sqlalchemy import Column


class BaseModel(Base):
    __abstract__ = True  # 主要是这一句起作用

    # 定制基本属性
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True, unique=True)  # 设置主键
    create_time = Column(DateTime, nullable=False, index=True)  # 创建时间
    update_time = Column(DateTime, nullable=False, index=True)  # 更新时间

    def __init__(self, id, create_time, update_time):
        self.id = id
        self.create_time = create_time
        self.update_time = update_time

    def __repr__(self):
        return "<BaseModel('%s','%s','%s')>" % (self.id, self.create_time, self.update_time)
