# 网络请求相关
import requests  # 用于发送HTTP请求，获取网页内容

# HTML解析相关
from bs4 import BeautifulSoup  # 用于解析HTML，提取所需数据

# 数据存储相关
import json  # 用于将数据保存为JSON格式
import pandas as pd  # 用于数据处理和保存为Excel格式

# 文件和路径处理
import os  # 用于处理文件路径和目录操作

class MovieScraper:
    def __init__(self, base_url='https://ssr1.scrape.center/page/'):
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.movies = []
    
    def get_total_pages(self):
        """获取总页数"""
        response = requests.get(self.base_url + '1', headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        pagination = soup.find('ul', class_='el-pager')
        if pagination:
            last_page = pagination.find_all('li')[-1].text
            return int(last_page)
        return 1
    
    def parse_movie(self, card):
        """解析单个电影信息"""
        name = card.find('h2', class_='m-b-sm').text.strip()
        categories = [cat.text.strip() for cat in card.find_all('button', class_='category')]
        info = card.find('div', class_='m-v-sm').text.strip()
        score = card.find('p', class_='score').text.strip()
        
        info_parts = info.split('/')
        region = info_parts[0].strip()
        duration = info_parts[1].strip()
        
        release_date_element = card.select_one('div.el-col-24.el-col-xs-9.el-col-sm-13.el-col-md-16 > div:nth-child(4) > span')
        release_date = release_date_element.text.strip() if release_date_element else ''
        
        return {
            '电影名': name,
            '类别': ' '.join(categories),
            '地区': region,
            '时长': duration,
            '上映时间': release_date,
            '评分': score
        }
    
    def scrape_page(self, page):
        """抓取单页数据"""
        url = self.base_url + str(page)
        print(f'正在抓取第 {page} 页...')
        
        try:
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            movie_cards = soup.find_all('div', class_='el-card__body')
            
            # 如果没有找到电影卡片，说明可能已经到达末页
            if not movie_cards:
                print(f'第 {page} 页没有找到电影数据，停止抓取')
                return None
            
            page_movies = []
            for card in movie_cards:
                movie = self.parse_movie(card)
                page_movies.append(movie)
            
            print(f'第 {page} 页抓取完成，获取到 {len(page_movies)} 部电影')
            return page_movies
        except Exception as e:
            print(f'抓取第 {page} 页时发生错误: {str(e)}')
            return None
    
    def scrape_all(self):
        """抓取所有页面数据"""
        total_pages = self.get_total_pages()
        print(f'总共有 {total_pages} 页')
        
        for page in range(1, total_pages + 1):
            page_movies = self.scrape_page(page)
            self.movies.extend(page_movies)
    
    def get_file_size(self, file_path):
        """获取文件大小并返回格式化的字符串"""
        size_bytes = os.path.getsize(file_path)
        # 如果文件小于1MB，显示KB
        if size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.2f} KB"
        # 如果文件大于等于1MB，显示MB
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    
    def save_to_json(self, filename='movies.json'):
        """保存为JSON文件"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, filename)
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.movies, f, ensure_ascii=False, separators=(',', ':'))
        
        file_size = self.get_file_size(json_path)
        print(f'数据已保存到 JSON 文件: {json_path} (文件大小: {file_size})')
    
    def save_to_excel(self, filename='movies.xlsx'):
        """保存为Excel文件"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        excel_path = os.path.join(current_dir, filename)
        
        df = pd.DataFrame(self.movies)
        df.to_excel(excel_path, index=False, engine='openpyxl')
        
        file_size = self.get_file_size(excel_path)
        print(f'数据已保存到 Excel 文件: {excel_path} (文件大小: {file_size})')

def main():
    # 创建爬虫实例
    scraper = MovieScraper()
    
    try:
        page = 1
        while True:
            # 抓取当前页面数据
            page_movies = scraper.scrape_page(page)
            
            # 如果抓取失败或没有数据，就停止
            if page_movies is None or len(page_movies) == 0:
                break
            
            # 添加到总数据中
            scraper.movies.extend(page_movies)
            page += 1
        
        # 如果成功抓取到数据才保存
        if scraper.movies:
            # 保存数据
            scraper.save_to_json()
            scraper.save_to_excel()
            print(f'成功抓取电影信息，共 {len(scraper.movies)} 部电影')
        else:
            print('没有抓取到任何电影信息')
            
    except Exception as e:
        print(f'发生错误: {str(e)}')
        import traceback
        print(traceback.format_exc())

if __name__ == '__main__':
    main()
