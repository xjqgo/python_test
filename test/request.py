import requests
from bs4 import BeautifulSoup
import re
import time
import pandas as pd

class MovieScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.example.com'
        }
        self.all_results = []

    def extract_text_content(self, url):
        """从指定的 URL 提取文本内容"""
        extracted_texts = []
        element_types = ['h2', 'span', 'p', 'button']
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # 检查请求是否成功
            soup = BeautifulSoup(response.text, 'html.parser')
            el_card_elements = soup.find_all(class_='el-card item m-t is-hover-shadow')
            for el_card_element in el_card_elements:
                seen_texts = set()
                for element_type in element_types:
                    elements = el_card_element.find_all(element_type)
                    for element in elements:
                        text_content = element.get_text()
                        cleaned_text = re.sub(r'\s+', '', text_content)
                        if len(cleaned_text) > 1 and cleaned_text not in seen_texts:
                            extracted_texts.append(cleaned_text)
                            seen_texts.add(cleaned_text)
        except requests.RequestException as e:
            print(f'请求失败：{e}')
        return extracted_texts

    def process_movies(self, texts):
        """处理提取的电影信息"""
        split_indices = [i for i, x in enumerate(texts) if isinstance(x, str) and x.replace('.', '', 1).isdigit()]
        result = []
        start = 0
        for end in split_indices:
            result.append(texts[start:end + 1])
            start = end + 1

        for movie in result:
            types = movie[1:-5]
            movie[1] = ','.join(types)
            del movie[2:len(movie) - 4]
            if len(movie) >= 5:
                movie[4] = movie[4].strip() if movie[4].strip() else "未知"
                date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
                match = date_pattern.search(movie[4])
                if match:
                    movie[4] = f"{match.group(0)} 上映"
                else:
                    movie[4] = "未知"
            else:
                movie.append("未知")
            while len(movie) < 6:
                movie.append(None)

        self.all_results.extend(result)

    def scrape(self, page_count):
        """执行抓取操作"""
        for i in range(1, page_count + 1):
            url = self.base_url + str(i)
            texts = self.extract_text_content(url)
            if texts:
                self.process_movies(texts)
            else:
                print(f"页面 {i} 提取失败")

    def save_to_excel(self, filename):
        """将提取的结果保存到 Excel 文件"""
        df = pd.DataFrame(self.all_results, columns=['电影名', '类型', '地区', '时长', '上映日期', '评分'])
        df.to_excel(filename, index=False)

if __name__ == "__main__":
    start_time = time.time()

    base_url = 'https://ssr1.scrape.center/page/'
    scraper = MovieScraper(base_url)
    scraper.scrape(page_count=10)
    scraper.save_to_excel('movies.xlsx')

    end_time = time.time()
    print(f"整个文件的执行时间：{end_time - start_time} 秒")