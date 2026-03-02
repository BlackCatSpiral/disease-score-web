from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import settings

# 数据库连接URL
DATABASE_URL = f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}?charset={settings.DB_CHARSET}"

# 创建引擎
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 依赖注入
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 数据模型 - 与原 tkinter 应用保持一致
class DiseaseScore(Base):
    __tablename__ = "disease_score"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    charge_category = Column(String(100), nullable=True, comment="收费分类")
    charge_item_code = Column(String(100), nullable=False, comment="收费项目编码")
    item_name = Column(String(200), nullable=False, comment="项目名称")
    province = Column(String(100), nullable=True, comment="省份")
    city = Column(String(100), nullable=True, comment="城市")
    original_price = Column(Float, nullable=True, comment="原价")
    discount_price = Column(Float, nullable=True, comment="折扣价")
    project_score = Column(Float, nullable=True, comment="项目分值")
    remark = Column(Text, nullable=True, comment="备注")
    create_time = Column(DateTime, default=datetime.now, comment="创建时间")
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
