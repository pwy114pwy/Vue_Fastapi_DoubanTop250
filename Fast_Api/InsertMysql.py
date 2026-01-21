# import_to_mysql.py
import pymysql
import csv

# 连接 MySQL
conn = pymysql.connect(
    host='localhost',
    port=13306,
    user='root',          # ← 改成你的用户名
    password='abc123',  # ← 改成你的密码
    database='douban_movies',
    charset='utf8mb4'
)
cursor = conn.cursor()

# 清空旧数据
cursor.execute("DELETE FROM movies")

# 读取 CSV 并插入
with open('./douban_top250.csv', 'r', encoding='utf-8-sig') as f:  # 使用 utf-8-sig 处理 BOM
    reader = csv.DictReader(f)
    for row in reader:
        # 处理列名可能包含 BOM 的情况
        rank_key = 'rank' if 'rank' in row else '\ufeffrank'
        
        # 处理导演字段，分离主演信息
        director = row['director']
        if '主演' in director:
            director = director.split('主演')[0].strip()
        
        cursor.execute("""
            INSERT INTO movies (rank, link, title, rating, year, country, director, genre)
            VALUES (%s,%s, %s, %s, %s, %s, %s, %s)
        """, (
            int(row[rank_key]),
            row['link'],
            row['title'],
            float(row['rating']),
            int(row['year']) if row['year'] and row['year'].isdigit() else None,
            row['country'],
            director,
            row['genre']
        ))

conn.commit()
cursor.close()
conn.close()
print("✅ 数据已导入 MySQL")