import pandas as pd

# 创建示例数据
data = {'Name': ['Alice', 'Bob', 'Charlie', 'David'],
        'Age': [25, 30, 35, 40],
        'Score': [85, 90, 88, 92]}
df = pd.DataFrame(data)

# 将数据写入 Excel 文件
df.to_excel('output.xlsx', index=False)