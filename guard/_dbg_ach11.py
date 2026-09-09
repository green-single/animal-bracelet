# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
c = open('app/static/animal.html', encoding='utf-8').read()
# 找批量解锁（unlockedCount++）
for m in re.finditer(r'unlockedCount\+\+', c):
    print('@', m.start())
    print(c[m.start()-500:m.start()+150])
    print('======')
