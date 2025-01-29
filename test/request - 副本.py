import requests
from bs4 import BeautifulSoup
import re
import time
import pandas as pd



class TextExtractor:
    def __init__(self, url, header):
        # 存储传入的 URL
        self.url = url
        # 存储传入的请求头
        self.header = header

    def extract_text_content(self):
        # 存储提取的文本列表
        extracted_texts = []
        # 查找的元素类型列表
        element_types = ['h2', 'span', 'p', 'button']
        # 发送 GET 请求到指定的 URL，并使用传入的请求头
        response = requests.get(self.url, headers=self.header)
        if response.status_code == 200:
            # 使用 BeautifulSoup 解析 HTML 内容，使用 html.parser 作为解析器
            soup = BeautifulSoup(response.text, 'html.parser')
            # 查找具有特定 class 的元素，这些元素是我们感兴趣的部分
            el_card_elements = soup.find_all(class_='el-card item m-t is-hover-shadow')
            for el_card_element in el_card_elements:
                # 存储在当前 el_card_element 中已经提取的文本，确保不重复
                seen_texts = set()
                for element_type in element_types:
                    # 在当前 el_card_element 中查找指定元素类型的元素
                    elements = el_card_element.find_all(element_type)
                    for element in elements:
                        # 获取元素的文本内容
                        text_content = element.get_text()
                        # 使用正则表达式将文本中的所有连续的空白字符（包括空格、换行符等）替换为空字符串
                        cleaned_text = re.sub(r'\s+', '', text_content)
                        if len(cleaned_text) > 1:
                            # 检查清理后的文本是否已经提取过
                            if cleaned_text not in seen_texts:
                                # 将不重复且长度大于 1 的文本添加到列表
                                extracted_texts.append(cleaned_text)
                                # 将提取过的文本添加到集合中
                                seen_texts.add(cleaned_text)
        else:
            # 请求失败时打印状态码
            print(f'请求失败，状态码：{response.status_code}')
        return extracted_texts


if __name__ == "__main__":
    # 记录开始时间
    start_time = time.time()
    # 定义请求头，模拟浏览器请求，避免被服务器识别为爬虫
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.example.com'
    }

    base_url = 'https://ssr1.scrape.center/page/'
    all_results = []
    for i in range(1, 11):
        # 生成完整的页面 URL
        url = base_url + str(i)
        # 创建 TextExtractor 类的实例
        extractor = TextExtractor(url, header)
        # 调用 extract_text_content 方法进行文本提取
        texts = extractor.extract_text_content()
        if texts:
            # 找到每个电影信息块的结束位置（评分的位置）
            split_indices = [i for i, x in enumerate(texts) if isinstance(x, str) and x.replace('.', '', 1).isdigit()]

            # 根据结束位置进行切片，分割到二维列表中
            result = []
            start = 0
            for end in split_indices:
                # 包含评分，所以 end + 1
                result.append(texts[start:end + 1])
                start = end + 1

            # 合并电影的类型字段
            for movie in result:
                # 提取电影的类型信息
                types = movie[1:-5]
                # 将类型信息用逗号连接，并存储在第 2 个位置
                movie[1] = ','.join(types)
                # 删除已经合并的类型信息
                del movie[2:len(movie) - 4]
                # 处理上映日期，如果为空，设置为 "未知"
                if len(movie) >= 5:
                    if not movie[4].strip():
                        movie[4] = "未知"
                else:
                    movie.append("未知")
                # 确保上映日期格式为 "YYYY-MM-DD 上映"，如果符合，将其修改为 "YYYY-MM-DD 上映" 的格式，否则设置为 "未知"
                if len(movie) >= 5:
                    import re
                    date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
                    match = date_pattern.search(movie[4])
                    if match:
                        movie[4] = f"{match.group(0)} 上映"
                    else:
                        movie[4] = "未知"
                else:
                    movie.append("未知")
                # 确保每个子列表长度为 6，不足的使用 "None" 填充
                while len(movie) < 6:
                    movie.append(None)
            all_results.extend(result)
        else:
            print(f"页面 {i} 提取失败")

    # 将处理后的子列表添加到 all_results 中
    # 最后，将 all_results 列表转换为 DataFrame，指定列名为 ['电影名', '类型', '地区', '时长', '上映日期', '评分']
    df = pd.DataFrame(all_results, columns=['电影名', '类型', '地区', '时长', '上映日期', '评分'])

    # 将 DataFrame 写入 Excel 文件
    print(df)
    df.to_excel('movies.xlsx', index=False)
    # 记录结束时间
    end_time = time.time()
    print(f"整个文件的执行时间：{end_time - start_time} 秒")