import json
import pandas as pd
import time
import os

def test_json_speed():
    start_time = time.time()
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'movies.json')
    
    print(f"正在读取JSON文件: {json_path}")
    with open(json_path, 'r', encoding='utf-8') as f:
        movies = json.load(f)
    
    print("\nJSON 数据最后3条示例:")
    for i, movie in enumerate(movies[-3:]):
        print(f"第 {len(movies)-2+i} 条: {movie['电影名']}")
    
    end_time = time.time()
    return end_time - start_time, len(movies)

def test_excel_speed():
    start_time = time.time()
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(current_dir, 'movies.xlsx')
    
    print(f"正在读取Excel文件: {excel_path}")
    df = pd.read_excel(excel_path, engine='openpyxl')
    movies = df.to_dict('records')
    
    print("\nExcel 数据最后3条示例:")
    for i, movie in enumerate(movies[-3:]):
        print(f"第 {len(movies)-2+i} 条: {movie['电影名']}")
    
    end_time = time.time()
    return end_time - start_time, len(movies)

def main():
    print("开始测试读取速度...")
    print("-" * 40)
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'movies.json')
    excel_path = os.path.join(current_dir, 'movies.xlsx')
    
    # 检查文件是否存在
    if not os.path.exists(json_path):
        print(f"错误: JSON文件不存在 - {json_path}")
        return
    if not os.path.exists(excel_path):
        print(f"错误: Excel文件不存在 - {excel_path}")
        return
    
    # 检查文件大小
    json_size = os.path.getsize(json_path) / 1024  # 转换为 KB
    excel_size = os.path.getsize(excel_path) / 1024  # 转换为 KB
    print(f"JSON 文件大小: {json_size:.2f} KB")
    print(f"Excel 文件大小: {excel_size:.2f} KB")
    
    print("-" * 40)
    
    # 测试 JSON 读取速度
    try:
        json_time, json_count = test_json_speed()
        print(f"\nJSON 文件读取时间: {json_time:.4f} 秒")
        print(f"JSON 数据总条数: {json_count}")
    except Exception as e:
        print(f"JSON 读取出错: {str(e)}")
        import traceback
        print(traceback.format_exc())
    
    print("-" * 40)
    
    # 测试 Excel 读取速度
    try:
        excel_time, excel_count = test_excel_speed()
        print(f"\nExcel 文件读取时间: {excel_time:.4f} 秒")
        print(f"Excel 数据总条数: {excel_count}")
    except Exception as e:
        print(f"Excel 读取出错: {str(e)}")
        import traceback
        print(traceback.format_exc())
    
    print("-" * 40)
    
    # 比较速度差异
    if 'json_time' in locals() and 'excel_time' in locals():
        diff = excel_time - json_time
        times = excel_time / json_time
        print(f"Excel 比 JSON 慢了 {diff:.4f} 秒")
        print(f"Excel 读取时间是 JSON 的 {times:.2f} 倍")

if __name__ == '__main__':
    main() 