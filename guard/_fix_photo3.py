# -*- coding: utf-8 -*-
"""照片白条修复（完整）：img自身aspect-ratio 4/3 铺满卡片"""
P = 'app/static/animal.html'
NL = chr(10)
c = open(P, encoding='utf-8').read()
lines = c.split(NL)

old_img = '.photo-wrap img { width: 100%; height: 110px; object-fit: cover; display: block; background: #e8e6df; }'
new_img = '.photo-wrap img { width: 100%; height: auto; aspect-ratio: 4/3; object-fit: cover; display: block; background: #e8e6df; }'
found = False
for i, l in enumerate(lines):
    if old_img in l:
        lines[i] = l.replace(old_img, new_img)
        found = True
        break
assert found, 'img未找到'

c = NL.join(lines)
open(P, 'w', encoding='utf-8').write(c)
# 验证
ok = 'aspect-ratio: 4/3' in c and 'height: 110px' not in c
print('照片修复写回:', 'OK' if ok else '检查失败')
