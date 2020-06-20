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

    # 单个对象
    def to_dict(self):
        _dic = {}
        for col_attr in self.__table__.columns:
            if isinstance(col_attr.type, DateTime):
                _dic[col_attr.name] = getattr(self, col_attr.name).strftime('%Y-%m-%d')
            else:
                _dic[col_attr.name] = getattr(self, col_attr.name)
        return _dic

    # 多个对象
    def dobule_to_dict(self):
        result = {}
        for key in self.__mapper__.c.keys():
            if getattr(self, key) is not None:
                result[key] = str(getattr(self, key))
            else:
                result[key] = getattr(self, key)
        return result

    def to_json(all_vendors):
        v = [ven.dobule_to_dict() for ven in all_vendors]
        return v
