# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
c = open('app/static/animal.html', encoding='utf-8').read()
print(c[136560:136920])
print('=== photo-wrap CSS ===')
i = c.find('.photo-wrap')
print(c[i-80:i+300])
