# -*- coding: utf-8 -*-
"""修复照片卡白条：img铺满4:3卡片 + 地图maxZoom限制"""
P = 'app/static/animal.html'
NL = chr(10)
c = open(P, encoding='utf-8').read()
lines = c.split(NL)

# 1. photo-wrap img 高度110px → 100%（铺满aspect-ratio卡片）
old_img = '.photo-wrap img { width: 100%; height: 110px; object-fit: cover; display: block; background: #e8e6df; }'
new_img = '.photo-wrap img { width: 100%; height: 100%; object-fit: cover; display: block; background: #e8e6df; }'
found = False
for i, l in enumerate(lines):
    if old_img in l:
        lines[i] = l.replace(old_img, new_img)
        found = True
        break
assert found, 'photo-wrap img未找到'

# 2. photo-wrap 加 height:100%
old_wrap = '.photo-wrap { position: relative; overflow: hidden; }'
new_wrap = '.photo-wrap { position: relative; overflow: hidden; height: 100%; }'
found = False
for i, l in enumerate(lines):
    if old_wrap in l:
        lines[i] = l.replace(old_wrap, new_wrap)
        found = True
        break
assert found, 'photo-wrap未找到'

# 3. 地图maxZoom限制（找Leaflet初始化）
import re
c2 = NL.join(lines)
# 找 maxZoom 相关
for m in re.finditer(r'maxZoom[^,}]*', c2):
    print('现有maxZoom:', m.group()[:60])
