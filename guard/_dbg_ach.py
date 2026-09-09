# -*- coding: utf-8 -*-
c = open('app/static/animal.html', encoding='utf-8').read()
# 看成就渲染区域（55943附近=HTML，97046附近=JS）
print('=== HTML (55850-56550) ===')
print(c[55850:56550])
