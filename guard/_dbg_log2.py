# -*- coding: utf-8 -*-
"""暴露调试变量"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
P = 'app/static/animal.html'
c = open(P, encoding='utf-8', newline='').read()
c = c.replace('\r\n', '\n')
OLD = "          if (lv2) liveHtml = '<div class=\"letter-item live\">"
NEW = "          window.__dbg = { lpt: lpt, curReg2: curReg2, lastReg2: lastReg2, days: days, ptsLen: pts.length, totalKm: totalKm, liveS2: liveS2, animalId: animalId, geoKeys: Object.keys(geoRefs || {}) };\n          if (lv2) liveHtml = '<div class=\"letter-item live\">"
if OLD in c:
    c = c.replace(OLD, NEW, 1)
    print('已暴露')
else:
    print('锚点未找到')
open(P, 'w', encoding='utf-8', newline='\n').write(c)
