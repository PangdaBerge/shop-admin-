# CLAUDE.md

## 项目概述

全栈商城管理系统 —— Vue 3 前端 + FastAPI Python 后端 + SQLite 数据库。

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端框架 | Vue 3 (Composition API) |
| 构建工具 | Vite 8 |
| 状态管理 | Pinia |
| 路由 | Vue Router 4 |
| CSS | Tailwind CSS 4 + PostCSS |
| HTTP 客户端 | Axios |
| 后端 | FastAPI (Python) |
| 数据库 | SQLite 3 |
| 包管理 | npm |

## 项目结构

```
shop-admin/
├── src/                    # Vue 前端源码
│   ├── assets/             # 静态资源（图片、SVG）
│   ├── components/         # 可复用 Vue 组件
│   ├── composables/        # Vue 组合式函数（hooks）
│   ├── router/             # Vue Router 配置
│   ├── store/              # Pinia 状态管理
│   ├── views/              # 页面级组件
│   ├── App.vue             # 根组件
│   ├── main.js             # 应用入口
│   └── style.css           # 全局样式
├── public/                 # 公共静态文件（不经过构建处理）
├── main.py                 # FastAPI 后端入口
├── init_db.py              # 数据库初始化脚本
├── update_db.py            # 数据库迁移/更新脚本
├── add_data.py             # 数据填充脚本
├── shop_system.db          # SQLite 数据库文件（不纳入版本控制）
├── index.html              # Vite 入口 HTML
├── vite.config.js          # Vite 配置
├── tailwind.config.js      # Tailwind 配置
├── postcss.config.js       # PostCSS 配置
└── package.json            # npm 依赖及脚本
```

## 常用命令

```bash
# 前端开发（Vite dev server）
npm run dev

# 前端生产构建
npm run build

# 预览生产构建
npm run preview

# 后端开发服务器
uvicorn main:app --reload

# 初始化数据库
python init_db.py

# 更新数据库
python update_db.py
```

## 编码规范

### 前端
- 使用 Vue 3 Composition API（`<script setup>`）
- 组件采用 PascalCase 命名
- 组合式函数以 `use` 为前缀（如 `useNotification`）
- 样式优先使用 Tailwind 工具类
- 路由视图按功能存放在 `views/` 目录

### 后端
- 遵循 FastAPI 最佳实践
- 使用 Pydantic 模型进行请求/响应验证
- 数据库操作使用原始 SQL（sqlite3），无 ORM
- 跨域配置在 `main.py` 中通过 CORSMiddleware 处理
