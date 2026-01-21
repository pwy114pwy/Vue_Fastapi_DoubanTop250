# 前端构建阶段
FROM node:18-alpine AS frontend-build

WORKDIR /app/frontend

# 复制前端依赖文件
COPY DouBan_Top205/package*.json ./

# 安装前端依赖
RUN npm install

# 复制前端源代码
COPY DouBan_Top205/ .

# 构建前端应用
RUN npm run build

# 后端构建阶段
FROM python:3.9-slim AS backend-build

WORKDIR /app/backend

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc-dev \
    libmariadb-dev \
    libmariadb-dev-compat \
    && rm -rf /var/lib/apt/lists/*

# 复制后端依赖文件
COPY Fast_Api/requirements.txt ./

# 安装后端依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制后端源代码
COPY Fast_Api/ .

# 最终运行阶段
FROM python:3.9-slim

WORKDIR /app

# 安装运行时依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmariadb3 \
    && rm -rf /var/lib/apt/lists/*

# 复制后端构建产物
COPY --from=backend-build /app/backend /app/backend

# 复制前端构建产物
COPY --from=frontend-build /app/frontend/dist /app/frontend/dist

# 安装 Gunicorn 用于生产环境
RUN pip install --no-cache-dir gunicorn

# 暴露端口
EXPOSE 8000

# 设置环境变量
ENV APP_ENV=production
ENV DEBUG=false

# 启动命令
CMD cd /app/backend && gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.main:app