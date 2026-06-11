import sqlite3
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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

class LoginRequest(BaseModel):
    username: str
    password: str

class ProductRequest(BaseModel):
    name: str
    price: float

# 新增：定义订单接收格式
class OrderRequest(BaseModel):
    total_price: float
    items_detail: str

@app.post("/api/login")
def login(request: LoginRequest):
    conn = get_db()
    user = conn.execute("SELECT id, username, role FROM users WHERE username = ? AND password = ?", (request.username, request.password)).fetchone()
    conn.close()
    if user:
        fake_token = f"{user['username']}-{user['role']}"
        return {"code": 200, "message": "登录成功", "data": {"token": fake_token, "user": {"name": user['username'], "role": user['role']}}}
    else:
        return {"code": 401, "message": "用户名或密码错误！"}

@app.get("/api/products")
def get_products():
    conn = get_db()
    products = conn.execute("SELECT * FROM products ORDER BY id ASC").fetchall()
    conn.close()
    return {"code": 200, "data": [dict(p) for p in products]}

@app.post("/api/products")
def add_product(product: ProductRequest, authorization: str = Header(None)):
    if not authorization or not authorization.endswith('-admin'):
        raise HTTPException(status_code=403, detail="权限不足")
    conn = get_db()
    conn.execute("INSERT INTO products (name, price) VALUES (?, ?)", (product.name, product.price))
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

# ================= 新增：订单管理 API =================

@app.post("/api/orders")
def create_order(order: OrderRequest, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="请先登录")
    # 从 token 中解析出是谁买的
    username = authorization.split('-')[0] 
    
    conn = get_db()
    conn.execute("INSERT INTO orders (username, total_price, items_detail) VALUES (?, ?, ?)", 
                 (username, order.total_price, order.items_detail))
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
        # 管理员可以看到所有人的订单
        orders = conn.execute("SELECT * FROM orders ORDER BY id DESC").fetchall()
    else:
        # 普通用户只能看到自己的订单
        orders = conn.execute("SELECT * FROM orders WHERE username = ? ORDER BY id DESC", (username,)).fetchall()
    conn.close()
    
    return {"code": 200, "data": [dict(o) for o in orders]}