import pandas as pd

try:
    # 读取Excel文件
    df = pd.read_excel('test/movies_cleaned.xlsx', engine='openpyxl')
    
    # 删除上映时间为空的行
    df = df.dropna(subset=['上映时间'])

    # 删除指定列中空格后面的字符
    df['电影名'] = df['电影名'].str.split().str[0]
    df['时长'] = df['时长'].str.split().str[0]
    df['上映时间'] = df['上映时间'].str.split().str[0]

    print(df)
    print(df.info())
    
    # 保存处理后的数据到新的Excel文件
    df.to_excel('test/movies_cleaned.xlsx', index=False)
    print("数据处理完成并已保存到新文件")
    
except FileNotFoundError:
    print("错误：找不到指定的Excel文件")
except PermissionError:
    print("错误：无法访问文件，可能文件正在被其他程序使用")
except KeyError as e:
    print(f"错误：找不到指定的列名 {e}")
except Exception as e:
    print(f"发生未预期的错误: {str(e)}")

# 将时长转换为数值类型
# df['时长'] = pd.to_numeric(df['时长'], errors='coerce')

# 找出时长最长的电影
longest_movie = df.loc[df['时长'].idxmax()]
print("\n时长最长的电影信息：")
print(f"电影名：{longest_movie['电影名']}")
print(f"时长：{longest_movie['时长']}分钟")
print(f"上映时间：{longest_movie['上映时间']}")

# 找出时长最短的电影
shortest_movie = df.loc[df['时长'].idxmin()]
print("\n时长最短的电影信息：")
print(f"电影名：{shortest_movie['电影名']}")
print(f"时长：{shortest_movie['时长']}分钟") 
print(f"上映时间：{shortest_movie['上映时间']}")

# 计算平均评分
average_rating = df['评分'].mean()
print(f"\n电影平均评分: {average_rating:.2f}")

# 找出评分高于平均分的电影
high_rated_movies = df[df['评分'] > average_rating]

print("\n评分高于平均分的电影:")
print(f"共有 {len(high_rated_movies)} 部电影评分高于平均分")
print("\n前5部高分电影:")
for _, movie in high_rated_movies.sort_values('评分', ascending=False).head().iterrows():
    print(f"电影名: {movie['电影名']}, 评分: {movie['评分']}, 上映时间: {movie['上映时间']}")

# 找出评分高于平均分且地区包含中国的电影
chinese_high_rated = df[(df['评分'] > average_rating) & (df['地区'].str.contains('中国', na=False))]

print("\n评分高于平均分的中国电影:")
print(f"共有 {len(chinese_high_rated)} 部中国电影评分高于平均分")
print("\n前5部高分中国电影:")
for _, movie in chinese_high_rated.sort_values('评分', ascending=False).head().iterrows():
    print(f"电影名: {movie['电影名']}, 评分: {movie['评分']}, 地区: {movie['地区']}")

# 找出2000年以后上映的电影
recent_movies = df[pd.to_datetime(df['上映时间']).dt.year >= 2000]

print("\n2000年以后上映的电影统计:")
print(f"共有 {len(recent_movies)} 部电影是2000年之后上映的")
print("\n按评分排序的前5部2000年后电影:") 
for _, movie in recent_movies.sort_values('评分', ascending=False).head().iterrows():
    print(f"电影名: {movie['电影名']}, 评分: {movie['评分']}, 上映时间: {movie['上映时间']}")

# 找出2010年以后上映的电影
recent_movies = df[pd.to_datetime(df['上映时间']).dt.year >= 2010]

print("\n2010年以后上映的电影统计:")
print(f"共有 {len(recent_movies)} 部电影是2010年之后上映的")
print("\n按评分排序的前5部2010年后电影:")
for _, movie in recent_movies.sort_values('评分', ascending=False).head().iterrows():
    print(f"电影名: {movie['电影名']}, 评分: {movie['评分']}, 上映时间: {movie['上映时间']}")



# 统计每年上映的电影数量
yearly_counts = df.groupby(pd.to_datetime(df['上映时间']).dt.year).size()

print("\n每年上映电影数量统计:")
print("-" * 40)
for year, count in yearly_counts.sort_index(ascending=False).items():
    print(f"{year}年: {count}部电影")
