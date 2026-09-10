# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
c = open('app/static/animal.html', encoding='utf-8').read()
print(c[15570:15850])
print('=== HTML 照片区 136400-136800 ===')
print(c[136400:136800])
