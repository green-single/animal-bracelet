# -*- coding: utf-8 -*-
import re
c = open('app/static/animal.html', encoding='utf-8').read()
m1 = list(re.finditer(r'L\.circleMarker\(points\[0\]', c))
m2 = list(re.finditer(r'L\.circleMarker\(points,', c))
print('points[0]出现:', len(m1))
print('points,出现:', len(m2))
# 完整行
for m in m2:
    line_end = c.find('\n', m.start())
    print(repr(c[m.start():line_end]))
# 82366前后
i = c.find('lineLayer = L.polyline')
line_end = c.find('\n', i)
line_start = c.rfind('\n', 0, i)
print('lineLayer块:')
print(repr(c[line_start:line_end]))
