# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
c = open('app/static/animal.html', encoding='utf-8', newline='').read()

# 找letters数组
i = c.find('letterList')
if i < 0:
    i = c.find('var letters')
print('letters定义位置:', i)
if i >= 0:
    print(c[i:i+2500])
