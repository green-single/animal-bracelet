# -*- coding: utf-8 -*-
c = open('app/static/animal.html', encoding='utf-8').read()
i = c.find('lineLayer = L.polyline')
seg = c[i:i + 300]
print(repr(seg))
print()
# 找circleMarker所有出现（含上下文）
import re
for m in re.finditer(r'L\.circleMarker\(points', c):
    print('@', m.start(), ':', c[m.start():m.start() + 60].replace('\n', ' '))
