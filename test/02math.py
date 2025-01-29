import math

# 取大小值
q, w, e = 1, 2, 7
print(min(q, w, e))
print(max(q, w, e))

# 模数
print(10 % 3)
print(11 % 3)
print(12 % 3)

# 幂次方
print(3 ** 2)  # 9
print(3 ** 3)  # 37
print(pow(3, 2))
print(pow(3, 3))

# 舍四进五
a = 2.5
s = 1.49
print(round(a), round(s))

# 绝对值
d = -2.1
print('绝对值', abs(d))

# 圆周率
print(math.pi)

# 圆的直径
r = float(input('输入圆的半径：'))  # 10=62.83
c = 2 * math.pi * r
print(f'圆的直径：{round(c, 2)}')

# 圆的面积
r = float(input('输入圆的半径：'))  # 20=1257
area = math.pi * (r ** 2)
print(f'圆的面积：{round(area)}')
