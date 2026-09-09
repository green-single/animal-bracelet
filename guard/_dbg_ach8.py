# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
c = open('app/static/animal.html', encoding='utf-8').read()
# 找批量解锁的items.forEach（104256附近往前）
i = c.find('// 更新UI')
print(c[i-100:i+600])
