from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "disease_score.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class DiseaseScore(Base):
    __tablename__ = "disease_score"
    
    id = Column(Integer, primary_key=True, index=True)
    charge_category = Column(String(100), nullable=True)
    charge_item_code = Column(String(100), nullable=False)
    item_name = Column(String(200), nullable=False)
    province = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    original_price = Column(Float, nullable=True)
    discount_price = Column(Float, nullable=True)
    project_score = Column(Float, nullable=True)
    remark = Column(Text, nullable=True)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
