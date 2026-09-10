# -*- coding: utf-8 -*-
"""照片修复最终版：百分比高度链铺满4:3卡片"""
P = 'app/static/animal.html'
NL = chr(10)
c = open(P, encoding='utf-8').read()
lines = c.split(NL)

# 1. wrap 加 height:100%（撑满aspect-ratio卡片）
old_wrap = '.photo-wrap { position: relative; overflow: hidden; }'
new_wrap = '.photo-wrap { position: relative; overflow: hidden; height: 100%; }'
found = False
for i, l in enumerate(lines):
    if old_wrap in l:
        lines[i] = l.replace(old_wrap, new_wrap)
        found = True
        break
assert found, 'wrap未找到'

# 2. img 改为 height:100% + object-fit:cover（去掉auto+aspect-ratio）
old_img = '.photo-wrap img { width: 100%; height: auto; aspect-ratio: 4/3; object-fit: cover; display: block; background: #e8e6df; }'
new_img = '.photo-wrap img { width: 100%; height: 100%; object-fit: cover; display: block; background: #e8e6df; }'
found = False
for i, l in enumerate(lines):
    if old_img in l:
        lines[i] = l.replace(old_img, new_img)
        found = True
        break
assert found, 'img未找到'

c = NL.join(lines)
open(P, 'w', encoding='utf-8').write(c)
print('OK 照片最终版写回')
i = c.find('.photo-wrap {')
print(repr(c[i:i+70]))
i2 = c.find('.photo-wrap img')
print(repr(c[i2:i2+110]))
