def is_prime(n):
    if n <= 1:  # 1 及以下的数不是素数
        return False
    if n <= 3:  # 2 和 3 是素数
        return True
    if n % 2 == 0 or n % 3 == 0:  # 能被 2 或 3 整除的数不是素数
        return False
    i = 5
    while i * i <= n:  # 检查到 i 的平方小于等于 n
        if n % i == 0 or n % (i + 2) == 0:  # 检查是否能被 i 或 i+2 整除
            return False
        i += 6  # 每次加 6 检查
    return True


for num in range(1, 101):
    if is_prime(num):
        print(num)
for i in range(1, 101):
    if is_prime(i):
        print(i)