# 南京中山陵景区导览管理系统 - FastAPI 后端

数据库名：`scenery`

## 功能范围

保留数据库课程设计需要的核心功能：

- 游客注册、登录、JWT 鉴权
- 南京中山陵景点浏览、搜索、详情
- 南京中山陵路线浏览、路线推荐、路线详情
- 收藏景点、取消收藏、我的收藏
- 反馈提交、我的反馈、管理员处理反馈
- FAQ 常见问题查询、管理员维护 FAQ
- 文本问答：优先匹配 FAQ，FAQ 无法回答时调用 DeepSeek API，失败时返回兜底回答
- 聊天记录保存和查询
- 管理员管理用户、中山陵景点、路线、FAQ、反馈、聊天记录

已删除/弱化数字人、情感分析、Dify 知识库、语音合成识别、天气等 AI 或外部接口功能。

## 启动方式

建议使用 Python 3.10、3.11 或 3.12。当前如果使用过新的 Python 预览版，FastAPI/Pydantic 依赖可能会出现兼容问题。

```bash
cd scenery_backend
pip install -r requirements.txt
copy .env.example .env
```

修改 `.env` 中的 MySQL 密码后启动：

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

首次启动会自动创建数据库 `scenery` 和数据表，并插入示例数据。

接口文档：

```text
http://127.0.0.1:8000/docs
```

## 默认管理员

- 账号：admin 或 13800000000
- 密码：Admin123456

## 后端目录结构

```text
scenery_backend/
├── main.py                 # FastAPI 入口，只负责初始化和挂载路由
├── core/
│   ├── config.py           # 环境变量、数据库、JWT、DeepSeek 配置
│   └── security.py         # 密码哈希、JWT 生成与解析
├── db/
│   ├── connection.py       # MySQL 连接和 get_db 依赖
│   ├── init_db.py          # 创建数据库 scenery 和数据表
│   └── seed.py             # 初始化管理员、中山陵景点、路线、FAQ 示例数据
├── dependencies/
│   └── auth.py             # 当前用户、管理员权限依赖
├── schemas/                # Pydantic 请求体模型
├── services/               # FAQ 匹配、DeepSeek 调用、路线组装、聊天流程
├── routers/
│   ├── tourist/            # 游客端接口包：注册登录、景点、路线、收藏、反馈、FAQ、聊天
│   └── admin/              # 管理端接口包：用户、景点、路线、FAQ、反馈、聊天记录管理
└── utils/
    └── response.py         # 统一返回和数据格式化
```

## 数据库课程设计体现点

- 实体：用户、景点、路线、路线景点关系、收藏、反馈、FAQ、聊天记录
- 约束：主键、外键、唯一约束、非空约束、枚举约束、CHECK 约束
- 模糊查询：景点搜索、FAQ 搜索、用户搜索
- 连接查询：收藏列表、路线详情、反馈列表、聊天记录
- 事务：注册、收藏、路线维护、文本问答记录保存
