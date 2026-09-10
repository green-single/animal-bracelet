# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
c = open('app/static/animal.html', encoding='utf-8', newline='').read()
# 找 adoptCardBtn / 领养相关按钮
for kw in ['adoptCardBtn', 'claimBtn', '领养', 'adoptCta', 'cta']:
    i = c.find(kw)
    if i >= 0:
        print(f'--- {kw} @ {i} ---')
        print(c[max(0,i-200):i+300])
        print()
