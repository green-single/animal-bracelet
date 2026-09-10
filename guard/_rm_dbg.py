# -*- coding: utf-8 -*-
"""移除调试代码"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
P = 'app/static/animal.html'
c = open(P, encoding='utf-8', newline='').read()
c = c.replace('\r\n', '\n')
OLD = "          window.__dbg = { lpt: lpt, curReg2: curReg2, lastReg2: lastReg2, days: days, ptsLen: pts.length, totalKm: totalKm, liveS2: liveS2, animalId: animalId, geoKeys: Object.keys(geoRefs || {}) };\n"
if OLD in c:
    c = c.replace(OLD, '', 1)
    print('已移除__dbg')
else:
    print('__dbg未找到')
open(P, 'w', encoding='utf-8', newline='\n').write(c)
