-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS douban_movies DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE douban_movies;

-- 创建 movies 表
CREATE TABLE IF NOT EXISTS movies (
    rank INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    rating REAL,
    year INTEGER,
    country TEXT,
    director TEXT,
    genre TEXT,
    link TEXT,
    poster_url TEXT,
    poster_path TEXT
);

-- 清空旧数据
DELETE FROM movies;

-- 导入数据
LOAD DATA INFILE '/docker-entrypoint-initdb.d/douban_top250.csv'
INTO TABLE movies
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(rank, link, title, rating, year, country, director, genre, poster_url, poster_path);

-- 添加索引
CREATE INDEX IF NOT EXISTS idx_movies_genre ON movies(genre);
CREATE INDEX IF NOT EXISTS idx_movies_year ON movies(year);
CREATE INDEX IF NOT EXISTS idx_movies_rating ON movies(rating);

-- 查看导入结果
SELECT COUNT(*) AS total_movies FROM movies;
SELECT * FROM movies LIMIT 10;