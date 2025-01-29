# 从random模块导入shuffle和choices函数
from random import shuffle,choices
# shuffle(): 当你需要随机打乱列表顺序时使用，比如洗牌游戏
# choices(): 当你需要随机抽样且允许重复时使用，比如模拟抽奖

# 定义一个包含字母的列表
data=['l','i','x','i']
# 打印原始列表
print(data)
# 随机打乱列表中的元素顺序
shuffle(data)
# 打印打乱后的列表
print(data)
# 从列表中随机选择一个元素并打印（返回的是一个只包含一个元素的列表）
print(choices(data))
# 从列表中随机选择3个元素并打印（返回的是一个包含3个元素的列表）
print(choices(data, k=3))
