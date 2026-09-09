# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
c = open('app/static/animal.html', encoding='utf-8').read()
# 往前找函数定义
i = c.find('ach[achId]) return;')
seg = c[:i]
import re
fns = [m.start() for m in re.finditer(r'function \w+', seg)]
print('最近函数:', c[fns[-1]:fns[-1]+120])
print()
print(c[i-700:i+50])
