# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
c = open('app/static/animal.html', encoding='utf-8').read()
print('=== 140700-141600 (年份UI) ===')
print(c[140700:141600])
