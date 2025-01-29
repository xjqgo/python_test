import pandas as pd

# 读取 Excel 文件
file_path = 'movies.xlsx'
df = pd.read_excel(file_path)

# 检查并修正特定行
# 这里假设 "类型" 和 "地区" 列索引为 1 和 2
for index, row in df.iterrows():
    if pd.isna(row.iloc[1]) and not pd.isna(row.iloc[2]):  # 如果类型为空且地区不为空
        df.at[index, df.columns[1]] = row.iloc[2]  # 将地区的值赋给类型
        df.at[index, df.columns[2]] = ''  # 清空地区的值

# 保存修正后的 DataFrame 回 Excel 文件
df.to_excel('movies_corrected.xlsx', index=False)