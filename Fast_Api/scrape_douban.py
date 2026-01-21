# scrape_douban.py
import requests
from bs4 import BeautifulSoup
import csv
import time
import re
import os
from urllib.parse import urljoin

# 配置
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
BASE_URL = "https://movie.douban.com/top250"
OUTPUT_FILE = "douban_top250.csv"
POSTER_DIR = "posters"  # 海报保存目录

def parse_movie_item(item):
    """解析单个电影条目"""
    try:
        # 排名
        rank_elem = item.find('em')
        rank = int(rank_elem.text.strip()) if rank_elem else None

        # 链接
        link_elem = item.find('a')  
        link = link_elem['href'] if link_elem else ""
        
        # 片名（主标题）
        title_elem = item.find('span', class_='title')
        title = title_elem.text.strip() if title_elem else ""
        
        # 评分
        rating_elem = item.find('span', class_='rating_num')
        rating = float(rating_elem.text.strip()) if rating_elem else 0.0
        
        # 海报链接
        img_elem = item.find('img')
        poster_url = img_elem['src'] if img_elem else ""
        
        # 解析 bd div 中的信息
        bd_elem = item.find('div', class_='bd')
        if bd_elem:
            p_elem = bd_elem.find('p', class_=None)  # 找到没有class的p标签
            if p_elem:
                p_text = p_elem.text.strip()
                
                # 分割文本，通常格式是：导演信息\n年份/国家/类型
                p_parts = p_text.split('\n')
                p_clean_parts = [part.strip() for part in p_parts if part.strip()]
                
                # 查找包含年份/国家/类型的那一行
                year_country_genre_line = ""
                for part in p_clean_parts:
                    if re.search(r'\d{4}', part):  # 查找包含年份的行
                        year_country_genre_line = part
                        break
                
                # 分离导演和年份/国家/类型信息
                director_match = re.search(r'导演:\s*([^/]+)', p_text)
                director = director_match.group(1).strip() if director_match else ""
                
                # 解析年份、国家、类型
                if year_country_genre_line:
                    # 提取年份
                    year_match = re.search(r'(\d{4})', year_country_genre_line)
                    year = int(year_match.group(1)) if year_match else None
                    
                    # 去掉年份后，按 '/' 分割
                    info_without_year = re.sub(r'\d{4}', '', year_country_genre_line).strip()
                    
                    # 按照豆瓣的格式：年份 / 国家 / 类型，分割后获取国家和类型
                    info_parts = [part.strip() for part in info_without_year.split('/') if part.strip()]
                    
                    # 国家通常是第一个非导演信息的部分
                    country = info_parts[0] if info_parts else ""
                    
                    # 类型是后续部分
                    genre = ",".join(info_parts[1:]) if len(info_parts) > 1 else ""
                else:
                    year = None
                    country = ""
                    genre = ""
            else:
                # 如果没找到p标签，使用默认值
                year = None
                country = ""
                genre = ""
                director = ""
        else:
            # 如果没找到bd div，使用默认值
            year = None
            country = ""
            genre = ""
            director = ""
        
        return {
            "rank": rank,
            "link": link,
            "title": title,
            "rating": rating,
            "year": year,
            "country": country,
            "director": director,
            "genre": genre,
            "poster_url": poster_url
        }
    except Exception as e:
        print(f"解析失败: {e}")
        return None

def download_poster(poster_url, movie_title, rank):
    """下载电影海报"""
    if not poster_url:
        return None
    
    # 创建海报目录（如果不存在）
    if not os.path.exists(POSTER_DIR):
        os.makedirs(POSTER_DIR)
    
    # 清理电影标题以用于文件名
    clean_title = re.sub(r'[<>:"/\\|?*]', '_', movie_title)  # 替换文件名中的非法字符
    # 限制文件名长度
    clean_title = clean_title[:50] if len(clean_title) > 50 else clean_title
    
    # 生成文件名
    file_extension = os.path.splitext(poster_url)[1]
    if not file_extension:
        file_extension = '.jpg'  # 默认扩展名
    filename = f"{rank:03d}_{clean_title}{file_extension}"
    filepath = os.path.join(POSTER_DIR, filename)
    
    try:
        response = requests.get(poster_url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"  📷 已保存海报: {filename}")
            return filepath
        else:
            print(f"  ❌ 海报下载失败: {poster_url} (状态码: {response.status_code})")
            return None
    except Exception as e:
        print(f"  ❌ 海报下载出错: {e}")
        return None

def scrape_douban_top250():
    all_movies = []
    
    for start in range(0, 250, 25):  # 10页，每页25部
        url = f"{BASE_URL}?start={start}&filter="
        print(f"正在爬取第 {start//25 + 1} 页...")
        
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code != 200:
                print(f"请求失败: {response.status_code}")
                break
                
            soup = BeautifulSoup(response.text, 'lxml')
            items = soup.find_all('div', class_='item')
            
            for item in items:
                movie = parse_movie_item(item)
                if movie:
                    all_movies.append(movie)
                    print(f"  已获取: {movie['rank']}. {movie['title']}")
                    
                    # 下载海报
                    poster_path = download_poster(movie['poster_url'], movie['title'], movie['rank'])
                    movie['poster_path'] = poster_path  # 保存本地路径
    
            time.sleep(2)  # 礼貌等待，避免被封
            
        except Exception as e:
            print(f"请求出错: {e}")
            break
    
    return all_movies

def save_to_csv(movies, filename):
    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:  # utf-8-sig 保证 Excel 正确显示中文
        fieldnames = ["rank", "link", "title", "rating", "year", "country", "director", "genre", "poster_url", "poster_path"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(movies)
    print(f"\n✅ 已保存 {len(movies)} 条数据到 {filename}")

if __name__ == "__main__":
    movies = scrape_douban_top250()
    if movies:
        save_to_csv(movies, OUTPUT_FILE)
        print(f"🖼️ 海报已保存到 '{POSTER_DIR}' 文件夹")
    else:
        print("❌ 未获取到任何数据")