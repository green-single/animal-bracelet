# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
c = open('app/static/animal.html', encoding='utf-8').read()
print('=== CSS 12900-13050 ===')
print(c[12900:13050])
print('=== CSS 15200-15600 (photo-card相关) ===')
print(c[15200:15600])
