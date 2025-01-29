age = int(input('请输入年龄：'))

if age <= 0:
    print('错误：年龄不能小于或等于0')
elif age < 18:
    print('您是未成年人')
elif age < 60:
    print('您是成年人')
elif age < 80:
    print('您是老年人')
elif age < 100:
    print('您是高龄老人2')
elif age >= 100:
    print('您是长寿老人1')
else:
    print('错误：年龄输入似乎过大')