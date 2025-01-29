# 定义 TShirt 和裤子的单价
tshirt_price = 56.5
pants_price = 89.8

# 从用户输入获取购买的 TShirt 和裤子的件数
tshirt_quantity = int(input("请输入购买的 TShirt 件数："))
pants_quantity = int(input("请输入购买的裤子件数："))

# 计算不打折时的总价
total_price = tshirt_quantity * tshirt_price + pants_quantity * pants_price
print(f"不打折时凤姐需要支付的总价为：{total_price:.2f} 元")

# 老板生日打 88 折的情况
discount_rate = 0.88
discounted_price = total_price * discount_rate
print(f"老板生日打 88 折时凤姐需要支付的总价为：{discounted_price:.2f} 元")