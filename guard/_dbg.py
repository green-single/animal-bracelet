# -*- coding: utf-8 -*-
c = open('app/static/animal.html', encoding='utf-8').read()
i = c.find('L.circleMarker(points')
print('find:', i)
if i >= 0:
    print(repr(c[i:i + 50]))
print('in检查:', 'L.circleMarker(points, { radius: 6' in c)
# 逐字符
seg = c[i:i + 30]
for ch in seg:
    print(repr(ch), end=' ')
