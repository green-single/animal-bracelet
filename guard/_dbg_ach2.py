# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
c = open('app/static/animal.html', encoding='utf-8').read()
# 找成就解锁JS
import re
for m in re.finditer(r'achievement-item|data-ach|unlocked', c):
    if m.start() > 95000:
        print('@', m.start(), ':', c[m.start()-80:m.start()+120].replace('\n', ' ')[:200])
        print()
