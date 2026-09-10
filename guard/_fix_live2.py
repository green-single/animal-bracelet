# -*- coding: utf-8 -*-
"""修复fresh作用域 + 随机来信改为'偶尔'（40%概率+每天最多一封）"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
P = 'app/static/animal.html'
c = open(P, encoding='utf-8', newline='').read()
c = c.replace('\r\n', '\n')

# ========== 1. 修复 fresh ==========
OLD1 = """          var liveS = {
            lat: _sfmt(lpt[1]), latH: lpt[1] >= 0 ? '°N' : '°S',
            lon: _sfmt(lpt[0]), lonH: lpt[0] >= 0 ? '°E' : '°W',
            totalKm: Math.round(totalKm),
            days: days,
            freshTxt: fresh,
            fmtD: fmtD(lts)
          };"""
NEW1 = """          var _da = 0;
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
assert OLD1 in c, 'liveS锚点未找到'
c = c.replace(OLD1, NEW1, 1)
print('fresh已修复')

# ========== 2. 随机来信概率化 ==========
OLD2 = """      } else {
        lv = genLiveLetter(liveS);
      }"""
NEW2 = """      } else {
        // 偶尔写信：40%概率 + 每天最多一封（避免每次刷新都有）
        var _todayS = new Date().toDateString();
        var _lastRand = null;
        try { _lastRand = localStorage.getItem('lr_rand_' + animalId); } catch (e) {}
        if (_lastRand !== _todayS && Math.random() < 0.4) {
          try { localStorage.setItem('lr_rand_' + animalId, _todayS); } catch (e) {}
          lv = genLiveLetter(liveS);
        }
      }"""
assert OLD2 in c, '随机来信锚点未找到'
c = c.replace(OLD2, NEW2, 1)
print('随机信概率化完成')

open(P, 'w', encoding='utf-8', newline='\n').write(c)
print('OK')
