from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from database import get_db, DiseaseScore

router = APIRouter(prefix="/records", tags=["记录管理"])

def to_dict(obj):
    """把 SQLAlchemy 对象转成字典"""
    return {
        "id": obj.id,
        "charge_category": obj.charge_category,
        "charge_item_code": obj.charge_item_code,
        "item_name": obj.item_name,
        "province": obj.province,
        "city": obj.city,
        "original_price": obj.original_price,
        "discount_price": obj.discount_price,
        "project_score": obj.project_score,
        "remark": obj.remark,
        "create_time": obj.create_time.isoformat() if obj.create_time else None,
        "update_time": obj.update_time.isoformat() if obj.update_time else None,
    }

@router.get("/")
def get_records(
    keyword: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """获取记录列表，支持搜索"""
    query = db.query(DiseaseScore)
    
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
    
    total = query.count()
    records = query.order_by(DiseaseScore.id).offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "data": [to_dict(r) for r in records]
    }

@router.get("/{record_id}")
def get_record(record_id: int, db: Session = Depends(get_db)):
    """获取单条记录"""
    record = db.query(DiseaseScore).filter(DiseaseScore.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="记录不存在")
    return to_dict(record)

@router.post("/")
def create_record(record: dict, db: Session = Depends(get_db)):
    """创建记录"""
    existing = db.query(DiseaseScore).filter(
        DiseaseScore.charge_item_code == record.get("charge_item_code")
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="收费项目编码已存在")
    
    db_record = DiseaseScore(**record)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return to_dict(db_record)

@router.put("/{record_id}")
def update_record(record_id: int, record: dict, db: Session = Depends(get_db)):
    """更新记录"""
    db_record = db.query(DiseaseScore).filter(DiseaseScore.id == record_id).first()
    if not db_record:
        raise HTTPException(status_code=404, detail="记录不存在")
    
    if record.get("charge_item_code"):
        existing = db.query(DiseaseScore).filter(
            DiseaseScore.charge_item_code == record["charge_item_code"],
            DiseaseScore.id != record_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="收费项目编码已存在")
    
    for key, value in record.items():
        if hasattr(db_record, key):
            setattr(db_record, key, value)
    
    db.commit()
    db.refresh(db_record)
    return to_dict(db_record)

@router.delete("/{record_id}")
def delete_record(record_id: int, db: Session = Depends(get_db)):
    """删除记录"""
    db_record = db.query(DiseaseScore).filter(DiseaseScore.id == record_id).first()
    if not db_record:
        raise HTTPException(status_code=404, detail="记录不存在")
    
    db.delete(db_record)
    db.commit()
    return {"message": "删除成功"}
