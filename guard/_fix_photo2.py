# -*- coding: utf-8 -*-
"""照片修复v2：img自身4:3铺满，去掉无效百分比"""
P = 'app/static/animal.html'
NL = chr(10)
c = open(P, encoding='utf-8').read()
lines = c.split(NL)

# 1. img: height:100% → aspect-ratio:4/3 + height:auto
old_img = '.photo-wrap img { width: 100%; height: 100%; object-fit: cover; display: block; background: #e8e6df; }'
new_img = '.photo-wrap img { width: 100%; height: auto; aspect-ratio: 4/3; object-fit: cover; display: block; background: #e8e6df; }'
found = False
for i, l in enumerate(lines):
    if old_img in l:
        lines[i] = l.replace(old_img, new_img)
        found = True
        break
assert found, 'img未找到'

# 2. photo-wrap: height:100% 改回（无害但清理）
old_wrap = '.photo-wrap { position: relative; overflow: hidden; height: 100%; }'
new_wrap = '.photo-wrap { position: relative; overflow: hidden; }'
found = False
for i, l in enumerate(lines):
    if old_wrap in l:
        lines[i] = l.replace(old_wrap, new_wrap)
        found = True
        break
assert found, 'wrap未找到'

c = NL.join(lines)
open(P, 'w', encoding='utf-8').write(c)
print('OK 照片v2完成')
