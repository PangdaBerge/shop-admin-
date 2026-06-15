import sqlite3
from pathlib import Path

# 数据库文件绝对路径 —— 无论从哪个目录启动都能正确找到
DB_PATH = Path(__file__).parent / 'shop_system.db'

# 连接数据库
conn = sqlite3.connect(str(DB_PATH))
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