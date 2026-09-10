# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
c = open('app/static/animal.html', encoding='utf-8').read()
# 找L.map和tileLayer
for kw in ['L.map(', 'tileLayer', 'L.tileLayer', 'maxZoom']:
    for m in re.finditer(re.escape(kw), c):
        print('@', m.start(), ':', c[m.start()-100:m.start()+200].replace('\n', ' ')[:300])
        print()
        break
