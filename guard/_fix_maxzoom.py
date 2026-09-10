# -*- coding: utf-8 -*-
"""地图maxZoom 17→16（避免偏远地区无卫星图）"""
P = 'app/static/animal.html'
c = open(P, encoding='utf-8').read()
n = c.count('maxZoom: 17')
c = c.replace('maxZoom: 17', 'maxZoom: 16')
open(P, 'w', encoding='utf-8').write(c)
print('maxZoom替换数:', n)
