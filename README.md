# HireFlow

智能招聘面试辅助系统 - 基于 FastAPI + Vue 3 + LangGraph 构建

## 功能特性

- **简历智能解析**: 自动提取简历信息，识别技能与经历
- **简历漏洞检测**: AI 分析简历中的潜在问题与风险点
- **面试辅助**: 实时语音转录，智能提问建议
- **可信度评估**: 评估候选人回答的可信度
- **评估报告**: 自动生成结构化面试评估报告
- **规章制度 RAG**: 基于企业文档的智能问答

## 技术栈

### 后端
- FastAPI - 高性能异步 Web 框架
- SQLAlchemy (async) - ORM 数据库操作
- PostgreSQL + pgvector - 关系型数据库与向量存储
- LangGraph - Agent 工作流编排
- Redis - 缓存与会话存储

### 前端
- Vue 3 + Vite - 现代化前端框架
- Element Plus - UI 组件库
- Pinia - 状态管理
- Vue Router - 路由管理

## 快速开始

### 环境要求
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose

### 1. 启动基础设施

```bash
docker-compose up -d
```

这将启动 PostgreSQL 和 Redis 服务。

### 2. 启动后端

```bash
cd backend

# 创建虚拟环境
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 复制环境变量配置
cp .env.example .env
# 编辑 .env 文件，配置 API 密钥等

# 初始化数据库
python scripts/init_db.py

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. 启动前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

访问 http://localhost:5173 查看应用。

## 项目结构

```
HireFlow/
├── backend/          # FastAPI 后端
├── frontend/         # Vue 3 前端
├── docs/            # 文档
├── models/          # 本地模型文件 (不提交 Git)
└── data/            # Docker 数据卷
```

## 开发规范

详见 `.cursorrules` 文件。

## 许可证

MIT License
