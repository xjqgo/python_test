# Python 中的一些高级数据类型（用于存储多个数据的类型）

# 列表[]list：有序，可重复，可扩展
z1 = ['l', 'x', '7', 'l', '7']
print(f'{z1} type：{z1.__class__.__name__}')
print(z1[0])

# 元组()tuple：有序，可重复，不可扩展
z2 = ('l', 'x', '7', 'l', '7')
print(f'{z2} type：{z2.__class__.__name__}')
print(z2[1])

# 集合{}set：无序，不可重复。可扩展
z3 = {'l', 'x', '7', 'l', '7'}
print(f'{z3} type：{z3.__class__.__name__}')

# 字典dict{a:21}：特点无序，不可重复。可扩展。
z4 = {"a": 'l', "q": 'x', "w": '7', 'e': 'l'}
print(f'{z4} type：{z4.__class__.__name__}')
print(z4['a'])