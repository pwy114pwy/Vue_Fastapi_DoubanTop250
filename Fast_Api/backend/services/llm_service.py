# backend/services/llm_service.py
import requests
from typing import Optional

OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "qwen3:1.7b"


def generate_sql_from_question(question: str, model: str = DEFAULT_MODEL) -> str:
    """
    使用 Ollama 调用 LLM 生成安全的 SQL 查询语句
    """
    prompt = f"""
只输出SQL查询语句，不要任何解释、分析或思考过程。
请务必记住以下内容：
数据库表结构：movies (title TEXT, rating REAL, year INTEGER, country TEXT, director TEXT, genre TEXT, rank INTEGER)

要求：
1. 只输出SQL，无解释,以及
2. 只允许SELECT，禁止危险操作
3. 用单引号包围字符串值
4. 对于 country、director、genre 字段：
   - 如果用户查询意图是“包含”“相关”“类似”等模糊语义，则使用 LIKE '%关键词%'
   - 如果用户明确指定“是”“等于”“类型为”“只包含”等精确语义，则使用 = '关键词'
   - 如果用户没有明确指定“是”“等于”“类型为”“只包含”等精确语义，则使用 LIKE '%关键词%'
7. 不要反引号、markdown标记
8. 不要换行，只输出一行
9. 不要包含<think>标签或任何思考内容
10. rating 和 year 用数字表示，其他都用中文表示
11. 必须使用 SELECT *
12.若用户的问题里出现图的类型，则忽略它


问题：{question+'/nothink'}
SQL：""".strip()

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.0,   # 最低随机性
            "top_p": 0.1,         # 限制采样范围
            "num_ctx": 1024,
        }
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=200)
        if response.status_code != 200:
            raise Exception(f"Ollama API error: {response.text}")

        result = response.json()

        raw_output = result.get("response", "").strip()
        print(f"原始输出: {raw_output}")

        # 移除<think>标签及其内容
        if "<think>" in raw_output:
            # 找到<think>和</think>的位置并移除中间内容
            start_tag = raw_output.find("<think>")
            end_tag = raw_output.find("</think>")
            if start_tag != -1 and end_tag != -1:
                # 移除<think>标签及其中间的内容
                cleaned_output = raw_output[:start_tag] + \
                    raw_output[end_tag + 8:]
                raw_output = cleaned_output.strip()

        # 移除markdown包裹
        if "```" in raw_output:
            start = raw_output.find("```")
            end = raw_output.find("```", start + 3)
            if end != -1:
                raw_output = raw_output[start+3:end].strip()
                # 如果是 ```sql 开头，去掉 sql
                if raw_output.lower().startswith("sql"):
                    raw_output = raw_output[3:].strip()

        # 移除可能的前缀如 "SQL:" 或 "答案："
        raw_output = raw_output.replace("SQL:", "").replace(
            "SQL：", "").replace("答案：", "").replace("答案:", "").strip()

        # 取第一行（确保只返回一行SQL）
        sql = raw_output.split("\n")[0].strip()

        # 只保留SQL语句部分（以分号或换行符结束）
        sql = sql.split(";")[0].strip()

        print(f"处理后SQL: {sql}")
        return sql

    except Exception as e:
        raise RuntimeError(f"LLM 调用失败: {str(e)}")
