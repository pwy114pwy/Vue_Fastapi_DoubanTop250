# D:\Fast_Api\backend\services\sql_safety.py

def is_safe_sql(sql: str) -> bool:
    """
    校验 SQL 是否安全（只允许 SELECT 查询 movies 表）
    """
    sql_upper = sql.upper().strip()
    
    # 必须是 SELECT 开头
    if not sql_upper.startswith("SELECT"):
        return False
    
    # 禁止危险操作
    dangerous = ["DROP", "DELETE", "UPDATE", "INSERT", "CREATE", "ALTER", "EXEC", "UNION", "JOIN"]
    if any(kw in sql_upper for kw in dangerous):
        return False
    
    # 必须查询 movies 表
    if "MOVIES" not in sql_upper:
        return False
        
    return True