# generate_db.py
import sqlite3
import csv
import os

# 配置路径
CSV_PATH = "./douban_top250.csv"      # ← 改成你的 CSV 路径
DB_PATH = "./backend/database/movies.db"  # 输出数据库路径

# 创建 data 目录（如果不存在）
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# 连接数据库
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 创建表
cursor.execute("""
CREATE TABLE IF NOT EXISTS movies (
    rank INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    rating REAL,
    year INTEGER,
    country TEXT,
    director TEXT,
    genre TEXT
)
""")

# 清空旧数据（可选）
cursor.execute("DELETE FROM movies")

# 读取 CSV 并插入数据
with open(CSV_PATH, "r", encoding="utf-8-sig") as f:  # 使用 utf-8-sig 来处理 BOM
    reader = csv.DictReader(f)
    
    for row in reader:
        print(row)
        
        # 处理可能包含主演信息的导演字段
        director = row["director"]
        if "主演" in director:
            # 只保留导演部分，去除主演信息
            director = director.split("主演")[0].strip()
        
        # 获取正确的列名（处理BOM）
        rank_key = 'rank' if 'rank' in row else '\ufeffrank'
        
        cursor.execute("""
        INSERT INTO movies (rank, title, rating, year, country, director, genre)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            int(row[rank_key]),
            row["title"],
            float(row["rating"]),
            int(row["year"]) if row["year"] else None,  # 处理空值
            row["country"],
            director,
            row["genre"]
        ))

# 提交并关闭
conn.commit()
conn.close()

print(f"✅ 数据库已生成: {DB_PATH}")
print(f"📊 共插入记录数: {cursor.rowcount}")