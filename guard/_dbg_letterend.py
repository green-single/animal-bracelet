# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
c = open('app/static/animal.html', encoding='utf-8', newline='').read()
i = c.find('百日之约')
print(repr(c[i-60:i+520]))
