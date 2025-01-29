z = float(input('体重：'))
unit = input('kg/lb').upper()
new_unit = ''

if unit == 'KG':
    z *= 2.2
    new_unit = '磅'
elif unit == 'LB':
    z /= 2.2
    new_unit = '公斤'
else:
    print('单位有误')

print(f'你的体重：{round(z)}{new_unit}')
