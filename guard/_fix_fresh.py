# -*- coding: utf-8 -*-
"""修复 fresh 作用域问题"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
P = 'app/static/animal.html'
c = open(P, encoding='utf-8', newline='').read()
c = c.replace('\r\n', '\n')

OLD = """          var liveS = {
            lat: _sfmt(lpt[1]), latH: lpt[1] >= 0 ? '°N' : '°S',
            lon: _sfmt(lpt[0]), lonH: lpt[0] >= 0 ? '°E' : '°W',
            totalKm: Math.round(totalKm),
            days: days,
            freshTxt: fresh,
            fmtD: fmtD(lts)
          };"""
NEW = """          var _da = 0;
          try { _da = Math.max(0, Math.floor((Date.now() - new Date(lts.replace(' ', 'T')).getTime()) / 86400000)); } catch (e) {}
          var _fresh = _da === 0 ? '今天，它刚刚更新了定位' : _da === 1 ? '昨天，它还在路上' : _da <= 7 ? _da + ' 天前，它留下了新的足迹' : '它正在一段安静的旅途中';
          var liveS = {
            lat: _sfmt(lpt[1]), latH: lpt[1] >= 0 ? '°N' : '°S',
            lon: _sfmt(lpt[0]), lonH: lpt[0] >= 0 ? '°E' : '°W',
            totalKm: Math.round(totalKm),
            days: days,
            freshTxt: _fresh,
            fmtD: fmtD(lts)
          };"""
assert OLD in c, 'liveS锚点未找到'
c = c.replace(OLD, NEW, 1)
open(P, 'w', encoding='utf-8', newline='\n').write(c)
print('已修复')
