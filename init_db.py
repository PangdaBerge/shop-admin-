import sqlite3

# 1. 连接到本地数据库文件（如果不存在会自动创建）
conn = sqlite3.connect('shop_system.db')
cursor = conn.cursor()

# 2. 强行一次性执行所有 SQL 语句
cursor.executescript('''
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user'
);

DROP TABLE IF EXISTS products;
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL
);

INSERT INTO users (username, password, role) VALUES 
('admin', '123456', 'admin'),
('zff', '123456', 'user');

INSERT INTO products (name, price) VALUES 
('ROG 高性能游戏本', 10999.00),
('Vicious 联名款单宁裤', 899.00),
('瓦洛兰特限定外设套装', 1299.00);
''')

# 3. 保存并关闭
conn.commit()
conn.close()

print("✅ 数据库 shop_system.db 初始化大功告成！表已建好，数据已就位！")