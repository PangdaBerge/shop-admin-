import sqlite3
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    conn = sqlite3.connect('shop_system.db')
    conn.row_factory = sqlite3.Row
    return conn


# ============== 数据模型 ==============

class LoginRequest(BaseModel):
    username: str
    password: str


class ProductRequest(BaseModel):
    name: str
    price: float
    category: str = '未分类'


class OrderRequest(BaseModel):
    total_price: float
    items_detail: str


class TaskCreateRequest(BaseModel):
    title: str
    description: str = ''
    status: str = 'todo'
    priority: str = 'medium'
    assignee: str = ''


class TaskUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    assignee: Optional[str] = None


# ============== 用户认证 ==============

@app.post("/api/login")
def login(request: LoginRequest):
    conn = get_db()
    user = conn.execute(
        "SELECT id, username, role FROM users WHERE username = ? AND password = ?",
        (request.username, request.password)
    ).fetchone()
    conn.close()
    if user:
        fake_token = f"{user['username']}-{user['role']}"
        return {
            "code": 200,
            "message": "登录成功",
            "data": {"token": fake_token, "user": {"name": user['username'], "role": user['role']}}
        }
    else:
        return {"code": 401, "message": "用户名或密码错误！"}


# ============== 商品管理 (含分类) ==============

@app.get("/api/products")
def get_products(category: Optional[str] = None):
    conn = get_db()
    if category and category != '全部':
        products = conn.execute(
            "SELECT * FROM products WHERE category = ? ORDER BY id ASC", (category,)
        ).fetchall()
    else:
        products = conn.execute("SELECT * FROM products ORDER BY id ASC").fetchall()
    conn.close()
    return {"code": 200, "data": [dict(p) for p in products]}


@app.get("/api/categories")
def get_categories():
    conn = get_db()
    categories = conn.execute("SELECT DISTINCT category FROM products ORDER BY category").fetchall()
    conn.close()
    return {"code": 200, "data": [c['category'] for c in categories]}


@app.post("/api/products")
def add_product(product: ProductRequest, authorization: str = Header(None)):
    if not authorization or not authorization.endswith('-admin'):
        raise HTTPException(status_code=403, detail="权限不足")
    conn = get_db()
    conn.execute(
        "INSERT INTO products (name, price, category) VALUES (?, ?, ?)",
        (product.name, product.price, product.category)
    )
    conn.commit()
    conn.close()
    return {"code": 200, "message": "上架成功！"}


@app.delete("/api/products/{product_id}")
def delete_product(product_id: int, authorization: str = Header(None)):
    if not authorization or not authorization.endswith('-admin'):
        raise HTTPException(status_code=403, detail="权限不足")
    conn = get_db()
    conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
    return {"code": 200, "message": "下架成功！"}


# ============== 订单管理 ==============

@app.post("/api/orders")
def create_order(order: OrderRequest, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="请先登录")
    username = authorization.split('-')[0]

    conn = get_db()
    conn.execute(
        "INSERT INTO orders (username, total_price, items_detail) VALUES (?, ?, ?)",
        (username, order.total_price, order.items_detail)
    )
    conn.commit()
    conn.close()
    return {"code": 200, "message": "支付成功！订单已写入数据库。"}


@app.get("/api/orders")
def get_orders(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="请先登录")

    username = authorization.split('-')[0]
    role = authorization.split('-')[1]

    conn = get_db()
    if role == 'admin':
        orders = conn.execute("SELECT * FROM orders ORDER BY id DESC").fetchall()
    else:
        orders = conn.execute(
            "SELECT * FROM orders WHERE username = ? ORDER BY id DESC", (username,)
        ).fetchall()
    conn.close()

    return {"code": 200, "data": [dict(o) for o in orders]}


# ============== 任务看板 API (用户隔离) ==============

@app.get("/api/tasks")
def get_tasks(
    status: Optional[str] = None,
    view: Optional[str] = None,
    username_filter: Optional[str] = None,
    authorization: str = Header(None)
):
    """
    获取任务列表 — 用户隔离核心逻辑

    普通用户: 始终只看自己创建的任务
    管理员:
      - 不传 view 参数 (默认): 只看自己的任务
      - view=all:               查看所有人的任务
      - view=user + username_filter=xxx: 查看指定用户的任务
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="请先登录")

    current_user = authorization.split('-')[0]
    role = authorization.split('-')[1]

    conn = get_db()

    if role == 'admin':
        if view == 'all':
            # 管理员团队视图 — 查看所有人的任务
            if status:
                tasks = conn.execute(
                    "SELECT * FROM tasks WHERE status = ? ORDER BY id DESC", (status,)
                ).fetchall()
            else:
                tasks = conn.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
        elif view == 'user' and username_filter:
            # 管理员查看特定用户的任务
            if status:
                tasks = conn.execute(
                    "SELECT * FROM tasks WHERE status = ? AND username = ? ORDER BY id DESC",
                    (status, username_filter)
                ).fetchall()
            else:
                tasks = conn.execute(
                    "SELECT * FROM tasks WHERE username = ? ORDER BY id DESC",
                    (username_filter,)
                ).fetchall()
        else:
            # 默认：管理员只看自己的任务
            if status:
                tasks = conn.execute(
                    "SELECT * FROM tasks WHERE status = ? AND username = ? ORDER BY id DESC",
                    (status, current_user)
                ).fetchall()
            else:
                tasks = conn.execute(
                    "SELECT * FROM tasks WHERE username = ? ORDER BY id DESC",
                    (current_user,)
                ).fetchall()
    else:
        # 普通用户：始终只能看自己创建的任务
        if status:
            tasks = conn.execute(
                "SELECT * FROM tasks WHERE status = ? AND username = ? ORDER BY id DESC",
                (status, current_user)
            ).fetchall()
        else:
            tasks = conn.execute(
                "SELECT * FROM tasks WHERE username = ? ORDER BY id DESC",
                (current_user,)
            ).fetchall()

    conn.close()
    return {"code": 200, "data": [dict(t) for t in tasks]}


@app.get("/api/users")
def get_users(authorization: str = Header(None)):
    """获取用户列表 — 供管理员任务筛选用"""
    if not authorization:
        raise HTTPException(status_code=401, detail="请先登录")

    role = authorization.split('-')[1]

    conn = get_db()
    if role == 'admin':
        users = conn.execute("SELECT DISTINCT username FROM users ORDER BY username").fetchall()
        conn.close()
        return {"code": 200, "data": [u['username'] for u in users]}
    else:
        conn.close()
        # 普通用户不需要用户列表（前端不会显示筛选器）
        return {"code": 200, "data": []}


@app.post("/api/tasks")
def create_task(task: TaskCreateRequest, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="请先登录")

    username = authorization.split('-')[0]

    conn = get_db()
    conn.execute(
        "INSERT INTO tasks (title, description, status, priority, assignee, username) VALUES (?, ?, ?, ?, ?, ?)",
        (task.title, task.description, task.status, task.priority, task.assignee, username)
    )
    conn.commit()
    conn.close()
    return {"code": 200, "message": "任务创建成功！"}


@app.put("/api/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdateRequest, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="请先登录")

    username = authorization.split('-')[0]
    role = authorization.split('-')[1]

    conn = get_db()
    existing = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail="任务不存在")

    # 权限校验：只有任务创建者或管理员可以修改
    if role != 'admin' and existing['username'] != username:
        conn.close()
        raise HTTPException(status_code=403, detail="无权修改他人任务")

    # 只更新传入的字段
    updates = {}
    for field in ['title', 'description', 'status', 'priority', 'assignee']:
        val = getattr(task, field)
        if val is not None:
            updates[field] = val

    if updates:
        set_clause = ', '.join(f"{k} = ?" for k in updates.keys())
        values = list(updates.values()) + [task_id]
        conn.execute(f"UPDATE tasks SET {set_clause} WHERE id = ?", values)
        conn.commit()

    conn.close()
    return {"code": 200, "message": "任务更新成功！"}


@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="请先登录")

    username = authorization.split('-')[0]
    role = authorization.split('-')[1]

    conn = get_db()
    existing = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail="任务不存在")

    # 权限校验：只有任务创建者或管理员可以删除
    if role != 'admin' and existing['username'] != username:
        conn.close()
        raise HTTPException(status_code=403, detail="无权删除他人任务")

    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return {"code": 200, "message": "任务删除成功！"}
