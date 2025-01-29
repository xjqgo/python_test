import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import os

def get_movies(url):
    # 发送 HTTP 请求
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    
    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 找到所有电影卡片
    movie_cards = soup.find_all('div', class_='el-card__body')
    
    movies = []
    for card in movie_cards:
        # 提取电影信息
        name = card.find('h2', class_='m-b-sm').text.strip()
        categories = [cat.text.strip() for cat in card.find_all('button', class_='category')]
        info = card.find('div', class_='m-v-sm').text.strip()
        score = card.find('p', class_='score').text.strip()
        
        # 解析地区和时长
        info_parts = info.split('/')
        region = info_parts[0].strip()
        duration = info_parts[1].strip()
        
        # 使用完整的选择器获取上映时间
        release_date_element = card.select_one('div.el-col-24.el-col-xs-9.el-col-sm-13.el-col-md-16 > div:nth-child(4) > span')
        release_date = release_date_element.text.strip() if release_date_element else ''
        
        # 整理电影信息
        movie = {
            '电影名': name,
            '类别': ' '.join(categories),  # 将类别列表转换为字符串
            '地区': region,
            '时长': duration,
            '上映时间': release_date,
            '评分': score
        }
        movies.append(movie)
    
    return movies

def get_total_pages(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    # 找到最后一个分页按钮的数字
    pagination = soup.find('ul', class_='el-pager')
    if pagination:
        last_page = pagination.find_all('li')[-1].text
        return int(last_page)
    return 1

def main():
    base_url = 'https://ssr1.scrape.center/page/'
    all_movies = []
    
    # 获取总页数
    total_pages = get_total_pages(base_url + '1')
    print(f'总共有 {total_pages} 页')
    
    # 抓取每一页的数据
    for page in range(1, total_pages + 1):
        url = base_url + str(page)
        print(f'正在抓取第 {page} 页...')
        movies = get_movies(url)
        all_movies.extend(movies)
        print(f'第 {page} 页抓取完成，获取到 {len(movies)} 部电影')
    
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 设置文件保存路径
    json_path = os.path.join(current_dir, 'movies.json')
    excel_path = os.path.join(current_dir, 'movies.xlsx')
    
    # 保存 JSON 文件
    try:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(all_movies, f, ensure_ascii=False, indent=2)
        print(f'JSON 文件已保存到: {json_path}')
    except Exception as e:
        print(f'保存 JSON 文件时出错: {e}')
    
    # 保存 Excel 文件
    try:
        df = pd.DataFrame(all_movies)
        df.to_excel(excel_path, index=False, engine='openpyxl')
        print(f'Excel 文件已保存到: {excel_path}')
    except Exception as e:
        print(f'保存 Excel 文件时出错: {e}')
    
    print(f'成功抓取所有页面，共 {len(all_movies)} 部电影信息')

if __name__ == '__main__':
    main()
