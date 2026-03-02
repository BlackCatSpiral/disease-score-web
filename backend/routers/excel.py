from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db, DiseaseScore
import pandas as pd
import io
from typing import Optional

router = APIRouter(prefix="/excel", tags=["Excel操作"])

# 字段映射（与原应用保持一致）
FIELD_MAPPING = {
    '收费分类': 'charge_category',
    '收费项目编码': 'charge_item_code',
    '项目名称': 'item_name',
    '省份': 'province',
    '城市': 'city',
    '原价': 'original_price',
    '折扣价': 'discount_price',
    '项目分值': 'project_score',
    '备注': 'remark'
}

REQUIRED_COLUMNS = ['收费项目编码', '项目名称']

@router.post("/import")
async def import_excel(
    mode: str,  # append/update/upsert/replace
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """导入Excel文件"""
    # 读取Excel
    try:
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"无法读取Excel文件: {str(e)}")
    
    # 检查必要列
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise HTTPException(status_code=400, detail=f"Excel缺少必要列: {missing}")
    
    # 字段映射
    df = df.rename(columns=FIELD_MAPPING)
    columns_to_keep = [v for v in FIELD_MAPPING.values() if v in df.columns]
    df = df[columns_to_keep].copy()
    df = df.where(pd.notnull(df), None)
    
    # 数值转换
    for col in ['original_price', 'discount_price', 'project_score']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    records = df.to_dict('records')
    
    result = {"inserted": 0, "updated": 0, "errors": []}
    
    if mode == 'append':
        # 追加模式
        for r in records:
            try:
                db_record = DiseaseScore(**r)
                db.add(db_record)
                result["inserted"] += 1
            except Exception as e:
                result["errors"].append(f"编码 {r.get('charge_item_code')}: {str(e)}")
        db.commit()
        
    elif mode == 'update':
        # 更新模式
        for r in records:
            existing = db.query(DiseaseScore).filter(
                DiseaseScore.charge_item_code == r['charge_item_code']
            ).first()
            if existing:
                for key, value in r.items():
                    if value is not None:
                        setattr(existing, key, value)
                result["updated"] += 1
        db.commit()
        
    elif mode == 'upsert':
        # 追加或更新
        for r in records:
            existing = db.query(DiseaseScore).filter(
                DiseaseScore.charge_item_code == r['charge_item_code']
            ).first()
            if existing:
                for key, value in r.items():
                    if value is not None:
                        setattr(existing, key, value)
                result["updated"] += 1
            else:
                db_record = DiseaseScore(**r)
                db.add(db_record)
                result["inserted"] += 1
        db.commit()
        
    elif mode == 'replace':
        # 替换模式（清空后导入）
        db.query(DiseaseScore).delete()
        for r in records:
            db_record = DiseaseScore(**r)
            db.add(db_record)
        result["inserted"] = len(records)
        db.commit()
    
    return result

@router.get("/export")
def export_excel(
    keyword: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """导出Excel文件"""
    from fastapi.responses import StreamingResponse
    
    query = db.query(DiseaseScore)
    
    # 搜索条件
    if keyword:
        from sqlalchemy import or_
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
    
    records = query.all()
    
    # 转换为DataFrame
    data = []
    for r in records:
        data.append({
            '收费分类': r.charge_category,
            '收费项目编码': r.charge_item_code,
            '项目名称': r.item_name,
            '省份': r.province,
            '城市': r.city,
            '原价': r.original_price,
            '折扣价': r.discount_price,
            '项目分值': r.project_score,
            '备注': r.remark
        })
    
    df = pd.DataFrame(data)
    if df.empty:
        # 返回模板
        df = pd.DataFrame(columns=list(FIELD_MAPPING.keys()))
    
    # 生成Excel
    output = io.BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=disease_score.xlsx"}
    )
