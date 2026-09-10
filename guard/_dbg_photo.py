# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
c = open('app/static/animal.html', encoding='utf-8').read()
# 照片卡片样式
for kw in ['photo-card', 'photoGrid', 'photo-item', 'photo-grid', 'photoList']:
    idxs = [m.start() for m in re.finditer(re.escape(kw), c)]
    print(kw, ':', idxs[:6])
