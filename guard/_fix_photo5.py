# -*- coding: utf-8 -*-
"""修复.photo-card img旧规则覆盖"""
P = 'app/static/animal.html'
NL = chr(10)
c = open(P, encoding='utf-8').read()
lines = c.split(NL)

old = '.photo-card img { width: 100%; height: 110px; object-fit: cover; display: block; background: #e8e6df; }'
new = '.photo-card img { width: 100%; height: 100%; object-fit: cover; display: block; background: #e8e6df; }'
found = False
for i, l in enumerate(lines):
    if old in l:
        lines[i] = l.replace(old, new)
        found = True
        break
assert found, '.photo-card img未找到'

c = NL.join(lines)
open(P, 'w', encoding='utf-8').write(c)
print('OK .photo-card img已改')
