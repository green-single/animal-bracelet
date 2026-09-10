# -*- coding: utf-8 -*-
"""随机来信概率化（40%+每天最多一封）"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
P = 'app/static/animal.html'
c = open(P, encoding='utf-8', newline='').read()
c = c.replace('\r\n', '\n')

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
open(P, 'w', encoding='utf-8', newline='\n').write(c)
print('概率化完成')
