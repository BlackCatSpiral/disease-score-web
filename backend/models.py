from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# 基础模型
class DiseaseScoreBase(BaseModel):
    charge_category: Optional[str] = None
    charge_item_code: str
    item_name: str
    province: Optional[str] = None
    city: Optional[str] = None
    original_price: Optional[float] = None
    discount_price: Optional[float] = None
    project_score: Optional[float] = None
    remark: Optional[str] = None

# 创建模型
class DiseaseScoreCreate(DiseaseScoreBase):
    pass

# 更新模型
class DiseaseScoreUpdate(BaseModel):
    charge_category: Optional[str] = None
    charge_item_code: Optional[str] = None
    item_name: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    original_price: Optional[float] = None
    discount_price: Optional[float] = None
    project_score: Optional[float] = None
    remark: Optional[str] = None

# 响应模型
class DiseaseScoreResponse(DiseaseScoreBase):
    id: int
    create_time: datetime
    update_time: datetime
    
    class Config:
        from_attributes = True

# 搜索请求
class SearchRequest(BaseModel):
    keyword: Optional[str] = None
    page: int = 1
    page_size: int = 50

# 批量导入请求
class ImportRequest(BaseModel):
    mode: str = Field(..., description="append/update/upsert/replace")
    data: list

# 数据库配置
class DBConfig(BaseModel):
    host: str = "localhost"
    port: int = 3306
    user: str = "root"
    password: str = ""
    database: str = "test"
    charset: str = "utf8mb4"
