# -*- coding: utf-8 -*-
"""随机来信概率 40% → 10%"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
P = 'app/static/animal.html'
c = open(P, encoding='utf-8', newline='').read()
c = c.replace('\r\n', '\n')
OLD = "if (_lastRand !== _todayS && Math.random() < 0.4) {"
NEW = "if (_lastRand !== _todayS && Math.random() < 0.1) {"
assert OLD in c, '概率锚点未找到'
c = c.replace(OLD, NEW, 1)
open(P, 'w', encoding='utf-8', newline='\n').write(c)
print('已改为10%')
