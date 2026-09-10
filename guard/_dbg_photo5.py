# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
c = open('app/static/animal.html', encoding='utf-8').read()
print('=== photo-item CSS (12400-12520) ===')
print(c[12400:12520])
print('=== photo-card相关所有CSS (15200-15320) ===')
print(c[15200:15320])
