import sqlite3
from pathlib import Path

# 数据库文件绝对路径 —— 无论从哪个目录启动都能正确找到
DB_PATH = Path(__file__).parent / 'shop_system.db'

# 1. 连接到本地数据库文件（如果不存在会自动创建）
conn = sqlite3.connect(str(DB_PATH))
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
    price REAL NOT NULL,
    category TEXT NOT NULL DEFAULT '未分类'
);

DROP TABLE IF EXISTS tasks;
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT DEFAULT '',
    status TEXT NOT NULL DEFAULT 'todo',
    priority TEXT NOT NULL DEFAULT 'medium',
    assignee TEXT DEFAULT '',
    username TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username, password, role) VALUES
('admin', '123456', 'admin'),
('zff', '123456', 'user');

INSERT INTO products (name, price, category) VALUES
('ROG 高性能游戏本', 10999.00, '电子产品'),
('Vicious 联名款单宁裤', 899.00, '服装'),
('瓦洛兰特限定外设套装', 1299.00, '电子产品'),
('机械键盘 Cherry 轴', 599.00, '电子产品'),
('纯棉 T 恤', 129.00, '服装'),
('进口零食大礼包', 199.00, '食品');

INSERT INTO tasks (title, description, status, priority, assignee, username) VALUES
('更新商品图片', '为所有商品拍摄并上传新的高清图片', 'todo', 'high', 'admin', 'admin'),
('优化页面加载速度', '压缩静态资源，启用懒加载', 'in_progress', 'medium', 'admin', 'admin'),
('审核用户订单', '检查今日订单是否有异常', 'todo', 'medium', 'zff', 'zff'),
('修复登录偶尔超时问题', '排查后端 token 过期逻辑', 'done', 'high', 'admin', 'admin');
''')

# 3. 保存并关闭
conn.commit()
conn.close()

print("✅ 数据库 shop_system.db 初始化大功告成！表已建好，数据已就位！")
print("   - users: 2 个用户")
print("   - products: 6 个商品 (含分类)")
print("   - tasks: 4 个任务 (看板)")
