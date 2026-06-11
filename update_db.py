import sqlite3

# 连接数据库
conn = sqlite3.connect('shop_system.db')
cursor = conn.cursor()

# 创建订单表 orders
cursor.executescript('''
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    total_price REAL NOT NULL,
    items_detail TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
''')

conn.commit()
conn.close()
print("✅ 订单表 (orders) 创建成功！支付数据库已就绪！")