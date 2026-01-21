# backend/api/v1/routes.py
from . import chart
from fastapi import APIRouter
from backend.services.llm_service import generate_sql_from_question
from backend.services.generate_chart_by_AI import generate_chart
from backend.services.sql_safety import is_safe_sql
from backend.database.db import execute_query
from fastapi import HTTPException

api_router = APIRouter()

# 包含图表路由
api_router.include_router(chart.router, prefix="/chart", tags=["chart"])

# 添加 ask 端点


@api_router.post("/ask")
def ask_movie_question(request: dict):
    question = request.get("question", "").strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question is required")

    try:
        # Step 1: LLM 生成 SQL
        raw_sql = generate_sql_from_question(question)
        print(f"Generated SQL: {raw_sql}")
        # Step 2: 安全校验
        if not is_safe_sql(raw_sql):
            raise HTTPException(
                status_code=400, detail="Generated SQL is unsafe or invalid")

        # Step 3: 执行查询
        results = execute_query(raw_sql)
        # print(f"Query results: {results}")
        chart_data = generate_chart(question, results)
        return {
            "question": question,
            "sql": raw_sql,
            "results": results,
            "chart_data": chart_data,
            "summary": f"共找到 {len(results)} 部电影。",
            "success": True
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")

from fastapi import FastAPI, Query

@api_router.get("/getlist")
async def get_movie_list():
    try:
        data_sql = f"SELECT * FROM movies"
        data_result = execute_query(data_sql)
        
        return {
            "results": data_result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取电影列表失败: {str(e)}")

