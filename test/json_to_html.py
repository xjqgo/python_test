import json
import os
from datetime import datetime

class HTMLGenerator:
    def __init__(self, json_file='movies.json'):
        self.json_file = json_file
        self.movies = self.load_json()
        
    def load_json(self):
        """加载JSON文件数据"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, self.json_file)
        
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def generate_html(self):
        """生成HTML内容"""
        html = f'''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>电影数据展示</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f0f2f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header {{
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .search-container {{
            margin: 20px 0;
        }}
        .search-input {{
            width: 100%;
            padding: 10px;
            font-size: 16px;
            border: 2px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }}
        .movie-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }}
        .movie-card {{
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .movie-card.highlight {{
            transform: scale(1.02);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            background-color: #fff3cd;
        }}
        .movie-title {{
            font-size: 18px;
            font-weight: bold;
            color: #1a1a1a;
            margin-bottom: 10px;
        }}
        .movie-info {{
            color: #666;
            margin-bottom: 5px;
        }}
        .movie-score {{
            color: #ff6b6b;
            font-weight: bold;
            font-size: 16px;
        }}
        .stats {{
            margin-bottom: 20px;
            color: #666;
        }}
        .timestamp {{
            color: #999;
            font-size: 14px;
        }}
        .no-results {{
            text-align: center;
            color: #666;
            padding: 20px;
            display: none;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>电影数据展示</h1>
            <div class="search-container">
                <input type="text" class="search-input" placeholder="输入电影名称、类别、地区等进行搜索..." id="searchInput">
            </div>
            <div class="stats">总共收录了 {len(self.movies)} 部电影</div>
            <div class="timestamp">生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        </div>
        <div class="no-results">未找到匹配的电影</div>
        <div class="movie-grid">
'''
        
        # 添加每部电影的卡片
        for movie in self.movies:
            html += f'''
            <div class="movie-card" data-title="{movie['电影名']}" data-category="{movie['类别']}" data-region="{movie['地区']}">
                <div class="movie-title">{movie['电影名']}</div>
                <div class="movie-info">类别：{movie['类别']}</div>
                <div class="movie-info">地区：{movie['地区']}</div>
                <div class="movie-info">时长：{movie['时长']}</div>
                <div class="movie-info">上映时间：{movie['上映时间']}</div>
                <div class="movie-score">评分：{movie['评分']}</div>
            </div>'''
        
        # 添加JavaScript代码和HTML结束标签
        html += '''
        </div>
    </div>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const searchInput = document.getElementById('searchInput');
            const movieCards = document.querySelectorAll('.movie-card');
            const noResults = document.querySelector('.no-results');
            let lastHighlighted = null;

            function searchMovies() {
                const searchTerm = searchInput.value.toLowerCase();
                let hasResults = false;

                movieCards.forEach(card => {
                    const title = card.dataset.title.toLowerCase();
                    const category = card.dataset.category.toLowerCase();
                    const region = card.dataset.region.toLowerCase();
                    
                    if (title.includes(searchTerm) || 
                        category.includes(searchTerm) || 
                        region.includes(searchTerm)) {
                        card.style.display = 'block';
                        hasResults = true;
                        
                        // 如果完全匹配电影名，高亮显示
                        if (title === searchTerm) {
                            if (lastHighlighted) {
                                lastHighlighted.classList.remove('highlight');
                            }
                            card.classList.add('highlight');
                            lastHighlighted = card;
                            
                            // 滚动到高亮的电影卡片
                            card.scrollIntoView({ behavior: 'smooth', block: 'center' });
                        }
                    } else {
                        card.style.display = 'none';
                    }
                });

                noResults.style.display = hasResults ? 'none' : 'block';
            }

            searchInput.addEventListener('input', searchMovies);
            
            // 添加按下回车键时的搜索功能
            searchInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    searchMovies();
                }
            });
        });
    </script>
</body>
</html>
'''
        return html
    
    def save_html(self, filename='movies.html'):
        """保存HTML文件"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(current_dir, filename)
        
        html_content = self.generate_html()
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f'HTML文件已生成：{html_path}')
        return html_path

def main():
    try:
        generator = HTMLGenerator()
        html_path = generator.save_html()
        
        # 自动在浏览器中打开生成的HTML文件
        import webbrowser
        webbrowser.open('file://' + os.path.abspath(html_path))
        
    except Exception as e:
        print(f'生成HTML时发生错误: {str(e)}')
        import traceback
        print(traceback.format_exc())

if __name__ == '__main__':
    main() 