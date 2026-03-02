# 病种分值管理系统 - Web 版

前后端分离架构：FastAPI + Vue 3 + MySQL

## 项目结构

```
disease-score-web/
├── backend/              # FastAPI 后端
│   ├── main.py          # 入口
│   ├── models.py        # 数据模型
│   ├── database.py      # 数据库连接
│   ├── config.py        # 配置文件
│   └── routers/         # API 路由
│       ├── records.py   # 记录管理
│       └── excel.py     # Excel 导入导出
├── frontend/            # Vue 3 前端
│   ├── src/
│   │   ├── components/  # 组件
│   │   ├── views/       # 页面
│   │   ├── api/         # API 接口
│   │   └── utils/       # 工具函数
│   └── package.json
└── docker-compose.yml   # 一键启动
```

## 快速开始

### 1. 后端启动

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### 2. 前端启动

```bash
cd frontend
npm install
npm run dev
```

### 3. Docker 启动（推荐）

```bash
docker-compose up -d
```

## 功能清单

- [x] 数据库连接配置
- [x] 数据增删改查
- [x] 搜索筛选（支持省份、城市、项目名称等）
- [x] Excel 导入（追加/更新/追加或更新/替换）
- [x] Excel 导出（支持按搜索结果导出）

## 与原文件兼容

- 数据库表结构保持一致（disease_score）
- Excel 模板格式一致
- 字段映射关系不变
