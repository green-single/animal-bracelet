# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
c = open('app/static/animal.html', encoding='utf-8', newline='').read()
i = c.find("d: 0, t: '初遇之信'")
print('信定义位置:', i)
if i >= 0:
    j = c.rfind('var', 0, i)
    start = c.rfind('[', j, i)
    print(c[start:i+2600])
