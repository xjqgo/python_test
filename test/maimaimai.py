#课堂练习：某超市TShirt的单价是56.5，裤子的单价是89.8,
# 凤姐买了3件TShirt,5条裤子，情写程序计算凤姐一共该给多少钱
#如果是老板生日，全场打88析，凤姐又需要付多少钱呢

# 定义 TShirt 和裤子的单价
tshirt_price = 56.5
pants_price = 89.8

# 计算不打折时的总价
total_price = 3 * tshirt_price + 5 * pants_price
print(f"不打折时凤姐需要支付的总价为：{total_price:.2f} 元")

# 老板生日打 88 折的情况
discount_rate = 0.88
discounted_price = total_price * discount_rate
print(f"老板生日打 88 折时凤姐需要支付的总价为：{discounted_price:.2f} 元")