# Docker 部署指南

本指南将介绍如何使用 Docker 和 Docker Compose 来构建和运行豆瓣电影 Top 250 可视化分析系统。

## 环境要求

- Docker 20.10.0 或更高版本
- Docker Compose 1.29.0 或更高版本

## 项目结构

```
Vue_Fastapi豆瓣top250/
├── Dockerfile          # 后端服务 Dockerfile
├── docker-compose.yml  # Docker Compose 配置文件
├── DOCKER.md           # Docker 部署指南
├── DouBan_Top205/      # 前端项目
└── Fast_Api/           # 后端项目
    ├── douban_top250.csv              # 电影数据 CSV 文件
    └── backend/database/init.sql      # 数据库初始化脚本
```

## 构建和运行

### 1. 克隆项目

```bash
git clone <项目仓库地址>
cd Vue_Fastapi豆瓣top250
```

### 2. 构建和启动容器

使用 Docker Compose 构建和启动所有服务：

```bash
docker-compose up -d --build
```

该命令会：
- 构建后端服务镜像
- 拉取并启动 MySQL 容器
- 拉取并启动 Ollama 容器
- 初始化数据库并导入电影数据
- 启动后端服务

### 3. 查看服务状态

```bash
docker-compose ps
```

### 4. 访问应用

- **后端 API**：http://localhost:8000
- **API 文档**：http://localhost:8000/docs
- **Ollama 服务**：http://localhost:11434

### 5. 停止服务

```bash
docker-compose down
```

## 服务说明

### MySQL 服务

- **容器名**：douban-mysql
- **端口**：13306:3306
- **数据库**：douban_movies
- **用户名**：douban
- **密码**：douban123
- **数据卷**：mysql-data（持久化存储）

### 后端服务

- **容器名**：douban-backend
- **端口**：8000:8000
- **环境变量**：
  - APP_ENV: production
  - DEBUG: false
  - DB_HOST: mysql
  - DB_PORT: 3306
  - DB_USER: douban
  - DB_PASSWORD: douban123
  - DB_NAME: douban_movies

### Ollama 服务

- **容器名**：douban-ollama
- **端口**：11434:11434
- **数据卷**：ollama-data（持久化存储模型）

## 数据初始化

数据库初始化过程：

1. MySQL 容器启动时，会执行 `backend/database/init.sql` 脚本
2. 脚本会创建 `douban_movies` 数据库和 `movies` 表
3. 然后从 `douban_top250.csv` 导入电影数据
4. 最后添加必要的索引以提高查询性能

## 常见问题

### 1. 数据库初始化失败

- 检查 `douban_top250.csv` 文件是否存在
- 检查 `init.sql` 脚本是否有语法错误
- 查看 MySQL 容器日志：
  ```bash
  docker-compose logs mysql
  ```

### 2. 后端服务无法连接到数据库

- 检查 MySQL 服务是否正常运行
- 检查后端服务的数据库配置是否正确
- 查看后端服务日志：
  ```bash
  docker-compose logs backend
  ```

### 3. AI 功能无法使用

- 检查 Ollama 服务是否正常运行
- 确保 Ollama 已拉取所需的模型（如 `qwen3:8b`）
- 查看 Ollama 容器日志：
  ```bash
  docker-compose logs ollama
  ```

### 4. 构建过程中遇到权限问题

- 确保当前用户有足够的权限执行 Docker 命令
- 在 Linux 系统上，可能需要使用 `sudo` 命令

## 自定义配置

### 1. 修改数据库配置

编辑 `docker-compose.yml` 文件中的 MySQL 服务配置：

```yaml
mysql:
  environment:
    MYSQL_ROOT_PASSWORD: your_root_password
    MYSQL_DATABASE: your_database_name
    MYSQL_USER: your_username
    MYSQL_PASSWORD: your_password
```

同时修改后端服务的数据库配置：

```yaml
backend:
  environment:
    DB_HOST: mysql
    DB_PORT: 3306
    DB_USER: your_username
    DB_PASSWORD: your_password
    DB_NAME: your_database_name
```

### 2. 修改端口映射

编辑 `docker-compose.yml` 文件中的端口映射：

```yaml
backend:
  ports:
    - "8080:8000"  # 将后端服务映射到 8080 端口

mysql:
  ports:
    - "3306:3306"  # 将 MySQL 映射到默认端口

ollama:
  ports:
    - "11434:11434"  # 将 Ollama 映射到默认端口
```

## 开发模式

### 1. 仅启动数据库和 Ollama 服务

```bash
docker-compose up -d mysql ollama
```

然后在本地启动前端和后端开发服务器：

- 前端：`cd DouBan_Top205 && npm run dev`
- 后端：`cd Fast_Api && python -m uvicorn backend.main:app --reload`

### 2. 查看日志

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend
```

## 生产环境部署

### 1. 使用环境变量文件

创建 `.env` 文件，存储敏感配置：

```env
# MySQL 配置
MYSQL_ROOT_PASSWORD=your_root_password
MYSQL_DATABASE=douban_movies
MYSQL_USER=douban
MYSQL_PASSWORD=your_password

# 后端配置
APP_ENV=production
DEBUG=false
DB_HOST=mysql
DB_PORT=3306
DB_USER=douban
DB_PASSWORD=your_password
DB_NAME=douban_movies
```

然后修改 `docker-compose.yml` 文件，使用环境变量文件：

```yaml
services:
  mysql:
    env_file: .env
  
  backend:
    env_file: .env
```

### 2. 优化性能

- **使用固定版本的镜像**：在 `docker-compose.yml` 中指定具体的镜像版本
- **限制资源使用**：为每个容器设置资源限制
- **启用健康检查**：添加健康检查配置

```yaml
backend:
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
    interval: 30s
    timeout: 10s
    retries: 3
  
mysql:
  healthcheck:
    test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
    interval: 30s
    timeout: 10s
    retries: 3
```

## 总结

使用 Docker 部署豆瓣电影 Top 250 可视化分析系统，可以：

- **简化部署**：一键构建和启动所有服务
- **环境隔离**：避免依赖冲突和环境差异
- **易于扩展**：可以轻松添加新的服务和功能
- **便于维护**：容器化管理，简化运维工作

通过本指南，您可以快速搭建一个完整的豆瓣电影 Top 250 可视化分析系统，包括前端、后端、数据库和 AI 服务。