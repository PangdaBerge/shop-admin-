import sqlite3
from pathlib import Path

# 数据库文件绝对路径 —— 无论从哪个目录启动都能正确找到
DB_PATH = Path(__file__).parent / 'shop_system.db'

# 连接数据库
conn = sqlite3.connect(str(DB_PATH))
cursor = conn.cursor()

try:
    # 批量插入新用户 (包含普通用户和管理员)
    cursor.executescript('''
    INSERT INTO users (username, password, role) VALUES 
    ('jett', '123456', 'user'),
    ('manager_01', 'admin123', 'admin'),
    ('cs_student', 'kaoyan2027', 'user');
    
    -- 批量插入新商品
    INSERT INTO products (name, price) VALUES 
    ('408计算机专业基础综合复习全书', 128.00),
    ('Valorant 7100特权点数充值卡', 500.00),
    ('Docker与容器化部署高级实战课程', 199.00),
    ('Trae AI 编程助手年度订阅', 399.00),
    ('AutoCAD 2026 商业正版授权', 2999.00),
    ('SolidWorks 机械设计标准件库', 99.00);
    ''')
    
    conn.commit()
    print("✅ 批量添加数据成功！新用户和新商品已全部入库！")
except sqlite3.IntegrityError:
    print("⚠️ 数据似乎已经添加过了，或者用户名重复啦！")
finally:
    conn.close()