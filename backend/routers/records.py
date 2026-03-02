from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import Optional
from database import get_db, DiseaseScore
from models import (
    DiseaseScoreCreate, 
    DiseaseScoreUpdate, 
    DiseaseScoreResponse,
    SearchRequest
)

router = APIRouter(prefix="/records", tags=["记录管理"])

@router.get("/", response_model=dict)
def get_records(
    keyword: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """获取记录列表，支持搜索"""
    query = db.query(DiseaseScore)
    
    # 搜索条件
    if keyword:
        like_pattern = f"%{keyword}%"
        query = query.filter(
            or_(
                DiseaseScore.charge_category.like(like_pattern),
                DiseaseScore.item_name.like(like_pattern),
                DiseaseScore.charge_item_code.like(like_pattern),
                DiseaseScore.province.like(like_pattern),
                DiseaseScore.city.like(like_pattern)
            )
        )
    
    # 分页
    total = query.count()
    records = query.order_by(DiseaseScore.id).offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "data": records
    }

@router.get("/{record_id}", response_model=DiseaseScoreResponse)
def get_record(record_id: int, db: Session = Depends(get_db)):
    """获取单条记录"""
    record = db.query(DiseaseScore).filter(DiseaseScore.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="记录不存在")
    return record

@router.post("/", response_model=DiseaseScoreResponse)
def create_record(record: DiseaseScoreCreate, db: Session = Depends(get_db)):
    """创建记录"""
    # 检查编码是否已存在
    existing = db.query(DiseaseScore).filter(
        DiseaseScore.charge_item_code == record.charge_item_code
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="收费项目编码已存在")
    
    db_record = DiseaseScore(**record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

@router.put("/{record_id}", response_model=DiseaseScoreResponse)
def update_record(record_id: int, record: DiseaseScoreUpdate, db: Session = Depends(get_db)):
    """更新记录"""
    db_record = db.query(DiseaseScore).filter(DiseaseScore.id == record_id).first()
    if not db_record:
        raise HTTPException(status_code=404, detail="记录不存在")
    
    # 检查编码是否与其他记录冲突
    if record.charge_item_code:
        existing = db.query(DiseaseScore).filter(
            DiseaseScore.charge_item_code == record.charge_item_code,
            DiseaseScore.id != record_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="收费项目编码已存在")
    
    # 更新字段
    update_data = record.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_record, key, value)
    
    db.commit()
    db.refresh(db_record)
    return db_record

@router.delete("/{record_id}")
def delete_record(record_id: int, db: Session = Depends(get_db)):
    """删除记录"""
    db_record = db.query(DiseaseScore).filter(DiseaseScore.id == record_id).first()
    if not db_record:
        raise HTTPException(status_code=404, detail="记录不存在")
    
    db.delete(db_record)
    db.commit()
    return {"message": "删除成功"}
