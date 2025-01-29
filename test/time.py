import time


def measure_time(func):
    def wrapper(*args, **kwargs):
        try:
            start_time = time.time()
            func(*args, **kwargs)
            end_time = time.time()
            print(f"函数 {func.__name__} 的运行时间为：{end_time - start_time} 秒")
        except Exception as e:
            print(f"函数 {func.__name__} 执行出错，错误信息：{e}")
    return wrapper


# 使用装饰器来测量函数运行时间
@measure_time
def my_function(count):
    for d in range(count):
        print(d)
    # 模拟函数的执行，这里可以替换为任何你需要的函数内容
    # time.sleep(2)


if __name__ == "__main__":
    # 记录整个文件开始运行的时间
    file_start_time = time.time()
    # 直接调用装饰后的函数
    my_function(100000)
    # 记录整个文件结束运行的时间
    file_end_time = time.time()
    print(f"整个文件的运行时间为：{file_end_time - file_start_time} 秒")