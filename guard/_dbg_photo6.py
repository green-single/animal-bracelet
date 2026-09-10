# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
c = open('app/static/animal.html', encoding='utf-8').read()
print(c[15200:15400])
# 看photo-zoom完整
i = c.find('.photo-zoom')
print('=== photo-zoom ===')
print(c[i:i+280])
