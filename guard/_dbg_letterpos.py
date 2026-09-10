# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
c = open('app/static/animal.html', encoding='utf-8', newline='').read()
i = c.find('letterList"')
# 往前找最近的 tab 容器
j = i
while j > 0:
    seg = c[max(0,j-300):j]
    k = seg.rfind('id="tab')
    if k >= 0:
        print('letterList最近的tab容器:', seg[k:k+60].split('"')[1])
        break
    j -= 300
# 找 letters 数组定义处的渲染起点（默认信）
i2 = c.find('{ d: 0, t: \'初遇之信\'')
# 往前找 'var letters' 或数组
j2 = c.rfind('var', 0, i2)
print('\n默认信数组附近:')
print(c[j2:i2+80])
