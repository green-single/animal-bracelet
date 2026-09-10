# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
c = open('app/static/animal.html', encoding='utf-8', newline='').read()
i = c.find('<body')
print('body开头:', repr(c[i:i+400]))
print()
# 找数据加载主流程
for kw in ['fetch(', 'loadAnimal', 'initMap', '_runAbcd', 'window.onload', 'DOMContentLoaded', 'showTab']:
    j = c.find(kw)
    print(f'{kw} @ {j} ctx: {repr(c[j:j+120]) if j>=0 else "无"}')
