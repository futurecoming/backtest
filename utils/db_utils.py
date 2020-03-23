import config
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def connent():
    """Returns data_spider connection and data_spider metadata object"""
    # We connect with the help of the PostgreSQL URL
    # postgresql+psycopg2://admin:admin@localhost:5432/test
    url = '{}://{}:{}@{}:{}/{}'
    url = url.format(config.DB_TYPE, config.DB_USER, config.DB_PWD, config.DB_HOST, config.DB_PORT, config.DB_NAME)

    # The return value of create_engine() is our connection object
    engine = sqlalchemy.create_engine(url, echo=True, client_encoding='utf8')

    # # We then bind the connection to MetaData()
    # meta = sqlalchemy.MetaData(bind=engine)

    return engine


# 初始化表
def init_db(engine):
    Base.metadata.create_all(engine)


# 删除表
def drop_db(engine):
    Base.metadata.drop_all(engine)


# 查询所有表
def list_tables(meta):
    for table in meta.tables:
        print(table)
    return meta.tables
