def calculate_factorial(n):
    """计算阶乘的函数，可以练习单步调试"""
    if n < 0:
        raise ValueError("负数没有阶乘")
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def process_list(numbers):
    """处理列表的函数，包含循环和条件判断"""
    processed = []
    for num in numbers:
        if num % 2 == 0:
            # 偶数加倍
            processed.append(num * 2)
        else:
            # 奇数加1
            processed.append(num + 1)
    return processed

def complex_calculation(x, y):
    """包含多个子函数调用的复杂计算"""
    def square(n):
        return n * n
    
    def add(a, b):
        return a + b
    
    result = square(x)  # 可以使用F7进入此函数
    result = add(result, square(y))  # 可以使用F8跳过此函数
    return result

def main():
    # 1. 测试阶乘计算 (可以在这里设置断点)
    print("测试阶乘计算：")
    try:
        num = 5
        result = calculate_factorial(num)
        print(f"{num}的阶乘是：{result}")
    except ValueError as e:
        print(f"错误：{e}")

    # 2. 测试列表处理 (可以使用Alt+F9运行到这里)
    print("\n测试列表处理：")
    numbers = [1, 2, 3, 4, 5]
    processed = process_list(numbers)
    print(f"原始列表：{numbers}")
    print(f"处理后的列表：{processed}")
    # 3. 测试复杂计算 (可以使用Shift+F8跳出子函数)
    print("\n测试复杂计算：")
    x, y = 3, 4
    result = complex_calculation(x, y)
    print(f"复杂计算结果：{result}")

if __name__ == "__main__":  
    # 在这里设置断点，然后按Shift+F9开始调试
    main() 
    print("程序结束 Git来了")
    print("程序结束 Git 4次保存")