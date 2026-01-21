# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .api.v1.routes import api_router

app = FastAPI(
    title="豆瓣电影可视化 API",
    debug=settings.DEBUG,
)

# CORS 设置（允许 Vue 开发服务器访问）
origins = ["http://localhost:5173"] if settings.APP_ENV == "development" else []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")